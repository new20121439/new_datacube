from django.shortcuts import render
from django.http import JsonResponse
from .tasks import add, run, add_then_square

# def TestCodeView(request):
#     x = request.GET['X']
#     y = request.GET['Y']
#     x, y = float(x), float(y)
#     # task = add.delay(x, y)
#     # task = run(x, y)
#     task = add_then_square(x, y)
#     return JsonResponse({
#         'Status': task.status,
#         'GetResult': task.get(),
#         'Result': task.result
#     })

import requests
from requests.auth import HTTPBasicAuth
from PIL import Image
import base64
from io import BytesIO

url = "https://scihub.copernicus.eu/dhus/odata/v1/Products('3bf6137d-1e97-4931-8276-872284a2cad8')/Products('Quicklook')/$value"
user = 'tranvandung20121439'
password = 'dung20121439'
def get_thumbnail(url):
    response = requests.get(url, auth=HTTPBasicAuth(user, password), stream=True)
    if response.status_code == 200:
        image = Image.open(response.raw)
        return image
    return None

def image_base64(im):
    if isinstance(im, str):
        im = get_thumbnail(im)
    with BytesIO() as buffer:
        im.save(buffer, 'jpeg')
        return base64.b64encode(buffer.getvalue()).decode()

def image_formatter(im):
    # return f'<img src="data:image/jpeg;base64,{image_base64(im)}">'
    return f"data:image/jpeg;base64,{image_base64(im)}"

def get_bas64im_from_url(url):
    response = requests.get(url, auth=HTTPBasicAuth(user, password), stream=True)
    b64_image = base64.b64encode(response.content)
    return f"data:image/jpeg;base64," + str(b64_image)

def TestCodeView(request):
    image = get_thumbnail(url)
    image = image_formatter(image)
    # image = get_bas64im_from_url(url)
    context = {'src': image}
    return render(request, "show_image.html", context)
