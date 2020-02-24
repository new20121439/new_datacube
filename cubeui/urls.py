"""cubeui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from pages.views import index

from api.query.views import QueryView
from api.download.views import DownloadView
from api.ingest.views import IngestData
from api.test_code.views import TestCodeView
# from api.scheduler.views import SchedulerView
# from api import upload

urlpatterns = [
    path('', index)
]

urlpatterns += [
    path('api/query', QueryView),
    path('api/download', DownloadView.as_view()),
    path('api/ingest', IngestData),
    path('api/test_code', TestCodeView),
    path('admin/', admin.site.urls),
    # path('api/scheduler', SchedulerView.as_view()),
    path('api/scheduler/', include('api.scheduler.urls')),
    path('api/upload/', include('api.upload.urls'))
]
