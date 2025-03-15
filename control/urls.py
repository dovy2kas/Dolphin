from django.urls import path
from .views import register, get_command, post_result, send_command_to_clients


urlpatterns = [
    path('register/', register),
    path('command/', get_command),
    path('result/', post_result),
    path('send_command/', send_command_to_clients),
]