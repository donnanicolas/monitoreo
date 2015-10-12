#Error msgs
BAD_JSON_RESPONSE = { 'result': 'error', 'message': 'Bad JSON payload' }
NO_CMD_RESPONSE = { 'result': 'error', 'message': 'No "cmd" parameter' }
NO_PID_RESPONSE = { 'result': 'error', 'message': 'No "pid" parameter' }
BAD_CMD_RESPONSE = { 'result': 'error', 'message': 'The CMD doesn\'t exists' }
NO_PRIORITY_RESPONSE = { 'result': 'error', 'message': 'No "priority" parameter' }
BAD_PS_PATCH_RESPONSE = { 'result': 'error', 'message': 'Bad Data' }
BAD_PATCH_PRIORITY_RESPONSE = { 'result': 'error', 'message': 'Bad Priority' }
NOT_ENOUGH_PERMISSION_RESPONSE = { 'result': 'error', 'message': 'No enough permissions for changing nice to process' }
BAD_PID_RESPONSE = { 'result': 'error', 'message': 'The PID is invalid' }
NO_PROCESS_PID_RESPONSE = { 'result': 'error', 'message': 'There is no process with the given PID' }
KILL_CURRENT_RESPONSE = { 'result': 'error', 'message': 'Can not kill current process' }
KILL_PARENT_RESPONSE = { 'result': 'error', 'message': 'Can not kill parent of current process' }
KILL_DENIED= {'result': 'error', 'message': 'No enough permissions to kill process'}
