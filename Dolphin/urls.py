from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel/', include('panel.urls')),
    path('control/', include('control.urls')),
]
