from django.http import JsonResponse
from django.views import View
from .services import list_aoi, create_aoi, get_aoi
import json


class List_CreateAOI(View):
    def get(self, request):
        response = list_aoi()
        return JsonResponse(response, safe=False)

    def post(self, request):
        body = json.loads(request.body)
        response = create_aoi(**body)
        return JsonResponse(response)


class Get_Update_DeleteAOI(View):
    def get(self, request, id):
        response = get_aoi(id)
        return JsonResponse(response)
