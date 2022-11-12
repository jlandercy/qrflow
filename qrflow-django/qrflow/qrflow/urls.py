from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static, serve

from qrflow import views

urlpatterns = [
    #re_path("r^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}, name="static-server"),
    path(r"media/<path:path>", views.FileServerView.as_view(), name="file-server"),
    path('admin/', admin.site.urls),
    path('account/', include(('django.contrib.auth.urls', 'django.contrib.auth'), namespace='account')),
    path('core/', include('core.urls', namespace="core")),
    path('', views.ProjectHomeView.as_view(), name='index'),
]

# Add prefix to classical URL:
urlpatterns = [path(f'{settings.URL_PREFIX}', include(urlpatterns))]

# Compose prefix in settings for specific URL:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
