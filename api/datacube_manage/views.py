from django.views import View
from .services import list_product
from django.http import JsonResponse


class DatacubeManageView(View):
    def get(self, request):
        response = list_product()
        return JsonResponse(
            response,
            safe=False
        )
