from django.urls import path
from .views import DatacubeManageView


urlpatterns = [
    path('', DatacubeManageView.as_view())
]
