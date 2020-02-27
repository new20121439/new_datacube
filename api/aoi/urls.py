from django.urls import path
from .views import List_CreateAOI, Get_Update_DeleteAOI


urlpatterns = [
    path('', List_CreateAOI.as_view()),
    path('<int:id>/', Get_Update_DeleteAOI.as_view())
]
