from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from stepik_vacancy import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vacancy.urls')),
    path('', include('account.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)