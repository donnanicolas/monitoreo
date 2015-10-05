from django.http import JsonResponse
from api.models import Key
from django.core.exceptions import ObjectDoesNotExist

class ApiKeyMiddleware(object):
    def process_request(self, request):
        if not request.get_full_path().startswith('/api'):
            return None

        if  'HTTP_AUTHORIZATION' not in request.META:
            return JsonResponse({'result': 'error', 'msg': 'Bad Auth'}, status=401)

        auth = request.META['HTTP_AUTHORIZATION']
        auth = auth.split(' ')
        if 2 != len(auth):
            return JsonResponse({'result': 'error', 'msg': 'Bad Auth'}, status=401)

        try:
            key = Key.objects.filter(key = auth[1]).get()
        except ObjectDoesNotExist as e:
            return JsonResponse({'result': 'error', 'msg': 'Bad Auth'}, status=401)
        return None
