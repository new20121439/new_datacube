from django.shortcuts import render
from django.views import View
import json
from .services import create_scheduler, list_scheduler, get_scheduler, update_scheduler, delete_scheduler
from django.http import JsonResponse


class List_CreateScheduleView(View):
    def get(self, request):
        response = list_scheduler()
        return JsonResponse(response, safe=False)

    def post(self, request):
        body = json.loads(request.body)
        response = create_scheduler(**body)
        return JsonResponse(response)

class Get_Update_DeleteSchedulerView(View):
    def get(self, request, id):
        response = get_scheduler(id)
        return JsonResponse(response)

    def put(self, request, id):
        body = json.loads(request.body)
        body.update({'id': id})
        response = update_scheduler(**body)
        return JsonResponse(response)

    def delete(self, request, id):
        print('asdadad Do this')
        response = delete_scheduler(id)
        return JsonResponse(response)
