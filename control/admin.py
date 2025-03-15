from django.contrib import admin
from .models import Client, Command

admin.site.register(Client)
admin.site.register(Command)