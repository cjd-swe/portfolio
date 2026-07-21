"""portfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, re_path
from django.views.static import serve
import jobs.views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', jobs.views.homepage, name = 'home'),
    path('jobs/<int:job_id>', jobs.views.detail, name = 'detail'),
    path('throughline/', jobs.views.throughline, name = 'throughline'),
    # Static files are served by whitenoise (see MIDDLEWARE); media (uploaded job
    # logos) is small and low-traffic enough to serve directly via Django here.
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
