"""job_success URL Configuration

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
from django.http import JsonResponse
from django.urls import path
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import subprocess
import os
from time import sleep
from django.conf import settings

BASH_PATH = os.path.join(settings.STATIC_DIR, 'bash')


def index(request):
    bat_files_path = [path for path in os.listdir(BASH_PATH) if '.bat' in path]
    context = {
        'commands': [path[:-4] for path in bat_files_path]
    }
    return render(request, 'index.html', context)


@csrf_exempt
def execute(request):
    command = request.POST.get('command')
    bash_file = os.path.join(BASH_PATH, command + ".bat")
    subprocess.call(bash_file)
    # sleep(30)

    return JsonResponse({
        "result": "created"
    }, status=201)


@csrf_exempt
def monitoring(request):
    command = request.POST.get('command')
    filename = f"output_{command}.txt"
    if os.path.exists(os.path.join(BASH_PATH, filename)):
        os.remove(os.path.join(BASH_PATH, filename))
        return JsonResponse({
            'is_existed': 'Yes'
        }, status=200)
    else:
        return JsonResponse({
            'is_existed': 'No'
        }, status=200)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('execute/', execute, name='execute'),
    path('monitoring/', monitoring, name='monitoring'),


]
