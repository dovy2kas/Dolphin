from django.urls import path

from . import views

urlpatterns = [
    path("", views.panel, name="panel"),
    path("payloads/", views.payloads, name="payloads"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]