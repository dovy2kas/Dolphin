from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from control.models import Client

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
  template = loader.get_template('payloads.html')
  return HttpResponse(template.render())

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