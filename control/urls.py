from django.urls import path
from .views import register, get_command, post_result, send_command_to_clients
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', register),
    path('command/', get_command),
    path('result/', post_result),
    path('send_command/', send_command_to_clients),
] + static('modules/', document_root=settings.UPLOADED_SCRIPTS_DIR)