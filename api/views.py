from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from subprocess import PIPE

import psutil, json, os, time, shlex, threading

from messages import *
from models import generate_key

'''
Base class for View
Avoids the CSRF check
'''
class NoCSRFView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(NoCSRFView, self).dispatch(*args, **kwargs)

class PsView(NoCSRFView):
    # GET /ps
    def get(self, request):
        processes = []

        for p in psutil.process_iter():
            processes.append(p.as_dict())

        return JsonResponse({'processes':processes, 'result': 'ok'})

    # POST /ps
    def post(self, request):
        try:
            data = received_json_data=json.loads(request.body)
        except Exception as e:
            return JsonResponse(BAD_JSON_RESPONSE, status=400)

        if 'cmd' not in data:
            return JsonResponse(NO_CMD_RESPONSE, status=400)

        cmd = data['cmd']
        # Random key for the output
        outputKey = generate_key()
        outfile = open('/tmp/' + outputKey + '.out','w')
        errfile = open('/tmp/' + outputKey + '.err','w')
        try:
            if '|' in cmd:
                cmd_parts = cmd.split('|')
                # Run the first part of the pipe
                p = psutil.Popen(shlex.split(cmd_parts[0]),stdin=None, stdout=PIPE, stderr=errfile)
                # Do the rest in background
                t = threading.Thread(target=runPipe, args=(cmd_parts[1:], p, outfile, errfile))
                t.start()
            else:
                # Run the command
                p = psutil.Popen(shlex.split(cmd), stdout=outfile, stderr=errfile)
                # Wait in background
                t = threading.Thread(target=runCmd, args=(p, outfile, errfile))
                t.start()
        except OSError as e:
            outfile.close()
            errfile.close()
            return JsonResponse(BAD_CMD_RESPONSE, status=400)
        return JsonResponse({'result': 'ok', 'process': p.pid, 'output': outputKey })

    # DELETE /ps
    def delete(self, request):
        try:
            data = received_json_data=json.loads(request.body)
        except Exception as e:
            return JsonResponse(BAD_JSON_RESPONSE, status=400)

        if 'pid' not in data:
            return JsonResponse(NO_PID_RESPONSE, status=400)

        try:
            pid = int(data['pid'])
        except Exception as e:
            return JsonResponse(BAD_PID_RESPONSE, status=400)

        # Abort if process doesn't exists
        if not psutil.pid_exists(pid):
            return JsonResponse(NO_PROCESS_PID_RESPONSE, status=400)

        current = psutil.Process(os.getpid())

        if current.pid == pid:
            return JsonResponse(KILL_CURRENT_RESPONSE, status=400)

        # We need to determine if the process is a parent before trying to kill it
        is_parent = False

        while True:

            if current.ppid() == pid:
                is_parent = True
                break

            if current.ppid() == 0:
                break

            current = psutil.Process(current.ppid())

        if is_parent:
            return JsonResponse(KILL_PARENT_RESPONSE, status=400)

        process = psutil.Process(pid)
        try:
            process.kill()
        except psutil.AccessDenied as e:
            return JsonResponse(KILL_DENIED, status=500)

        return JsonResponse({'result':'ok'})

    # PUT /ps
    def patch(self, request):
        try:
            data = received_json_data=json.loads(request.body)
        except Exception as e:
            return JsonResponse(BAD_JSON_RESPONSE, status=400)

        if 'pid' not in data:
            return JsonResponse(NO_PID_RESPONSE, status=400)

        if 'priority' not in data:
            return JsonResponse(NO_PRIORITY_RESPONSE, status=400)

        try:
            pid = int(data['pid'])
            priority = int(data['priority'])
        except Exception as e:
            return JsonResponse(BAD_PS_PATCH_RESPONSE, status=400)

        if priority > 20 or priority < -20:
            return JsonResponse(BAD_PATCH_PRIORITY_RESPONSE, status=400)

        if not psutil.pid_exists(pid):
            msg = 'No process with pid :' + str(pid)
            return JsonResponse({ 'result': 'error', 'message': msg }, status=400)
        process = psutil.Process(pid)

        try:
            process.nice(priority)
        except psutil.AccessDenied as e:
            return JsonResponse(NOT_ENOUGH_PERMISSION_RESPONSE, status=400)

        return JsonResponse({'result': 'ok'})

class ProcessView(NoCSRFView):
    # GET /ps/:pid
    def get(self, request, process):

        try:
            pid = int(process)
        except Exception as e:
            return JsonResponse(BAD_PID_RESPONSE, status=400)

        if not psutil.pid_exists(pid):
            return JsonResponse(NO_PROCESS_PID_RESPONSE, status=400)

        current = psutil.Process(os.getpid())
        return JsonResponse({'process': current.as_dict(), 'result': 'ok'})

class UserView(NoCSRFView):

    # GET /users
    def get(self, request):
        users = {}

        for p in psutil.process_iter():
            name = p.username()
            if name not in users:
                users[name] = {
                    'username': name,
                    'running': 1
                }
                continue

            users[name]['running'] += 1

        user_list = []

        for u in users:
            user_list.append(users[u])

        return JsonResponse({'users': user_list, 'result': 'ok'})

class UserTaskView(NoCSRFView):
    # GET /users/:username/ps
    def get(self, request, user):
        processes = []
        for p in psutil.process_iter():

            if p.username() != user:
                continue
            processes.append(p.as_dict())

        return JsonResponse({'processes':processes, 'result': 'ok'})

class ProcessOutputView(NoCSRFView):
    # GET /api/ps/output/:output
    def get(self, request, output):
        outfile = open('/tmp/' + output + '.out', 'r')
        errfile = open('/tmp/' + output + '.err', 'r')
        response = {
            'out': "".join(line.rstrip() for line in outfile),
            'err': "".join(line.rstrip() for line in errfile),
        }
        outfile.close()
        errfile.close()
        return JsonResponse(response)

'''
Function that runs in background to log the output of the process
'''
def runCmd(p, outfile, errfile):
    #Kill after a while
    waitKillClose(p, outfile, errfile)

'''
Function that runs the parts of the pipes in the background
'''
def runPipe(cmds, firstPipe, outfile, errfile):
    i = 0
    ps = {}

    # If only one pipe use the first process input and the exist file

    if len(cmds) == 1 :
        try:
            p=psutil.Popen(shlex.split(cmds[0]),stdin=firstPipe.stdout, stdout=outfile, stderr=errfile)
            waitKillClose(p, outfile, errfile)
        except OSError as e:
            errfile.write(str(e))
            outfile.close()
            errfile.close()
        return

    try:
        for cmd_part in cmds:
            cmd_part = cmd_part.strip()
            #In the first use the first process input
            if i == 0:
                ps[i]=psutil.Popen(shlex.split(cmd_part),stdin=firstPipe.stdout, stdout=PIPE, stderr=errfile)
            #If the last pipe to the outfile
            elif i == len(cmds) - 1:
                ps[i]=psutil.Popen(shlex.split(cmd_part),stdin=ps[i-1].stdout, stdout=outfile, stderr=errfile)
            #Else use the previous input and PIPE to the next
            else:
                ps[i]=psutil.Popen(shlex.split(cmd_part),stdin=ps[i-1].stdout, stdout=PIPE, stderr=errfile)
            i=i+1
    except OSError as e:
        errfile.write(str(e))
        if i-1 in ps:
            waitKillClose(ps[i-1], outfile, errfile)
            return
        outfile.close()
        errfile.close()
    else:
        waitKillClose(ps[i-1], outfile, errfile)

def waitKillClose(p, outfile, errfile):
    time.sleep(10)
    if p.poll() is not None:
        try:
            p.kill()
        except Exception as e:
            pass

    outfile.close()
    errfile.close()
