from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from places.views import show_places


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', show_places)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
