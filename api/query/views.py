from django.http import JsonResponse
from .tasks import query_task
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(["POST"])
def QueryView(request):
    body = json.loads(request.body)
    response = query_task(**body)
    return JsonResponse(
        response
    )

def get_platform_producttype(product_name):
    if product_name == "sentinel_2_l2a":
        return {
            'platformname': 'Sentinel-2',
            'product_type': 'S2MSI2A'
        }
    elif product_name == "sentinel_1_grd_50m_beta0":
        return {
            'platformname': 'Sentinel-1',
            'product_type': 'GRD'
        }
    else:
        raise Exception("Do not have this product. Please, choose another option")