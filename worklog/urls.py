from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from worklog import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('worklog_webapi.urls')),
    path('api/v1/', include('worklog_restapi.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
