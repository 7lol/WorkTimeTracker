from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('worklog.urls')),
    path('', include('worklog_webapi.urls')),
    path('api/v1/', include('worklog_restapi.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
