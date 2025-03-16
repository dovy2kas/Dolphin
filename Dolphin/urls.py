from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel/', include('panel.urls')),
    path('control/', include('control.urls')),
]


if settings.DEBUG:
    urlpatterns += static('/compiled_payloads/', document_root=os.path.join(settings.BASE_DIR, 'compiled_payloads'))