from django.http import JsonResponse
from django.views import View
from .tasks import download_process
import json
from .services import list_download


class DownloadView(View):

    def post(self, request):
        body = json.loads(request.body)
        response = download_process(**body)
        return JsonResponse(response)

    def get(self, request):
        response = list_download()
        return JsonResponse(response, safe=False)