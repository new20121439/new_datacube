from django.views import View
from .services import list_uploads, create_upload, get_upload
from django.http import JsonResponse


class ListCreate_Upload(View):
    def get(self, request):
        response = list_uploads()
        return JsonResponse(response, safe=False, )

    def post(self, request):
        body = request.POST
        print('dasdaddddddddddd', request.FILES['file'])
        kwargs = {
            'title': body['title'],
            'product_name': body['product_name'],
            'file': request.FILES['file']
        }
        response = create_upload(**kwargs)
        return JsonResponse(response)


class GetUpdateDelete_Upload(View):
    def get(self, request, id):
        response = get_upload(id)
        return JsonResponse(response)
