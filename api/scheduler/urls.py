from django.urls import path
from .views import List_CreateScheduleView, Get_Update_DeleteSchedulerView


urlpatterns = [
    path('', List_CreateScheduleView.as_view()),
    path('<int:id>/', Get_Update_DeleteSchedulerView.as_view())
]