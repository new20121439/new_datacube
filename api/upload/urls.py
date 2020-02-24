from django.urls import path, re_path
from .views import ListCreate_Upload, GetUpdateDelete_Upload

urlpatterns = [
    path('', ListCreate_Upload.as_view()),
    path('<int:id>/', GetUpdateDelete_Upload.as_view())
]