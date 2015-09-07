from django.http import JsonResponse
from api.models import Key
from django.core.exceptions import ObjectDoesNotExist

class ApiKeyMiddleware(object):
    def process_request(self, request):
        if not request.get_full_path().startswith('/api'):
            return None

        if  'key' not in request.REQUEST:
            return JsonResponse({'result': 'error', 'msg': 'No API key'}, status=400)

        try:
            key = Key.objects.filter(key = request.REQUEST.get('key')).get()
        except ObjectDoesNotExist as e:
            return JsonResponse({'result': 'error', 'msg': 'Bad API key'}, status=400)
        return None
