from django.http import JsonResponse
from .tasks import ingest_data


def IngestData(request):
    product_name = request.GET['product_name']
    uuid = request.GET['uuid']
    dataset_path = request.GET['dataset_path']
    print(product_name)
    status = ingest_data(product_name, dataset_path, uuid)
    return JsonResponse({
        'status': status
    })