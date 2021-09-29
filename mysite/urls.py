from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('chat.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
