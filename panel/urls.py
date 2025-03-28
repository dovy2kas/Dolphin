from django.urls import path

from . import views

urlpatterns = [
    path("", views.panel, name="panel"),
    path("payloads/", views.payloads, name="payloads"),
    path("modules/", views.modules, name="modules"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('send_command_to_clients/', views.send_command_to_clients, name='send_command_to_clients'),
]