# all the imports
import sqlite3
from flask import Flask, Response, request, g, redirect, url_for, abort, jsonify, request
import psutil, json, os

# configuration
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

def respond_with_error(msg, status=400):
    js = json.dumps({
        'error': msg,
        'status': status,
        'result': 'error'
    })
    return Response(js, status, mimetype='application/json')

@app.route('/ps', methods=['GET'])
def ps():
    processes = []

    for p in psutil.process_iter():
        processes.append(p.as_dict())

    print processes
    return jsonify(processes=processes, result='ok')

@app.route('/users', methods=['GET'])
def users():
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


    return jsonify(users=user_list, result='ok')

@app.route('/users/<string:user>/tasks', methods=['GET'])
def user_tasks(user):
    processes = []

    for p in psutil.process_iter():
        if p.username() != user:
            continue
        processes.append(p.as_dict())

    print processes
    return jsonify(processes=processes, result='ok')

@app.route('/ps', methods=['POST'])
def popen():
    data = request.get_json(silent=True)

    if data is None:
        abort(400)

    if 'cmd' not in data:
        abort(400)

    cmd = [data['cmd']]

    if 'args' in data:
        cmd = cmd + data['args']

    psutil.Popen(cmd)

    return jsonify(result='ok')

@app.route('/ps', methods=['DELETE'])
def kill():
    data = request.get_json(silent=True)

    if data is None:
        abort(400)

    if 'pid' not in data:
        return respond_with_error('No pid')

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

    return jsonify(result='ok')

@app.route('/ps', methods=['PUT'])
def nice():
    data = request.get_json(silent=True)

    if data is None:
        abort(400)

    if 'pid' not in data:
        return respond_with_error('No pid')

    if 'priority' not in data:
        return respond_with_error('No priority')

    try:
        pid = int(data['pid'])
        priority = int(data['priority'])
    except Exception as e:
        return respond_with_error('Bad data')

    if priority > 20 or priority < -20:
        return respond_with_error('Priority has to be between -20 and 20')

    if not psutil.pid_exists(pid):
        return respond_with_error('No process with pid :' + str(pid))

    process = psutil.Process(pid)

    try:
        process.nice(priority)
    except psutil.AccessDenied as e:
        return respond_with_error('No enough permission for changing nice to process: ' + str(pid))

    return jsonify(result='ok')

if __name__ == '__main__':
    app.run()
