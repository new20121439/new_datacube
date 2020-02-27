from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader


def index(request):
    print(1)
    template = loader.get_template('dist/index.html')
    context = {}
    return HttpResponse(template.render(context, request))