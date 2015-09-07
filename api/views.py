from django.shortcuts import render
from django.http import JsonResponse
import psutil, json, os
from django.views.decorators.http import require_http_methods
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#Error msgs
BAD_JSON_RESPONSE = { 'result': 'error', 'message': 'Bad JSON payload' }
NO_CMD_RESPONSE = { 'result': 'error', 'message': 'No "cmd" parameter' }
NO_PID_RESPONSE = { 'result': 'error', 'message': 'No "pid" parameter' }
NO_PRIORITY_RESPONSE = { 'result': 'error', 'message': 'No "priority" parameter' }
BAD_PS_PATCH_RESPONSE = { 'result': 'error', 'message': 'Bad Data' }
BAD_PATCH_PRIORITY_RESPONSE = { 'result': 'error', 'message': 'Bad Priority' }
NOT_ENOUGH_PERMISSION_RESPONSE = { 'result': 'error', 'message': 'No enough permission for changing nice to process' }

class NoCSRFView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(NoCSRFView, self).dispatch(*args, **kwargs)

class PsView(NoCSRFView):
    def get(self, request):
        processes = []

        for p in psutil.process_iter():
            processes.append(p.as_dict())

        return JsonResponse({'processes':processes, 'result': 'ok'})

    def post(self, request):
        try:
            data = received_json_data=json.loads(request.body)
        except Exception as e:
            return JsonResponse(BAD_JSON_RESPONSE, status=400)

        if 'cmd' not in data:
            return JsonResponse(NO_CMD_RESPONSE, status=400)

        cmd = [data['cmd']]

        if 'args' in data:
            cmd = cmd + data['args']

        p = psutil.Popen(cmd)

        return JsonResponse({'result': 'ok', 'process': p.pid})

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
            return respond_with_error('Bad pid')

        if not psutil.pid_exists(pid):
            return respond_with_error('No process with pid :' + str(pid))

        current = psutil.Process(os.getpid())

        if current.pid == pid:
            return respond_with_error('Can not kill current process')

        is_parent = False

        while True:

            if current.ppid() == pid:
                is_parent = True
                break

            if current.ppid() == 0:
                break

            current = psutil.Process(current.ppid())

        if is_parent:
            return respond_with_error('Can not kill parent of current process')

        process = psutil.Process(pid)
        process.kill()

        return JsonResponse({'result':'ok'})

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

class UserView(View):
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

class UserTaskView(View):
    def get(self, request, user):
        processes = []

        for p in psutil.process_iter():
            if p.username() != user:
                continue
            processes.append(p.as_dict())

        return JsonResponse({'processes':processes, 'result': 'ok'})
