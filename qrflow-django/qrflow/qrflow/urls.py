from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static, serve

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from qrflow import views


schema_view = get_schema_view(
   openapi.Info(
      title="QR-Flow API",
      default_version='v1.0',
      description="QR-Flow Management API",
      terms_of_service="https://www.landercy.be/terms/",
      contact=openapi.Contact(email="info@qrflow.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    #re_path("r^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}, name="static-server"),
    path(r"media/<path:path>", views.FileServerView.as_view(), name="file-server"),
    path('admin/', admin.site.urls),
    path('account/', include(('django.contrib.auth.urls', 'django.contrib.auth'), namespace='account')),
    path('api-auth/', include('rest_framework.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('core/', include('core.urls', namespace="core")),
    path('pki/', include('pki.urls', namespace="pki")),
    path('flow/', include('flow.urls', namespace="flow")),
    path('', views.ProjectHomeView.as_view(), name='index'),
]

# Add prefix to classical URL:
urlpatterns = [path(f'{settings.URL_PREFIX}', include(urlpatterns))]

# Compose prefix in settings for specific URL:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
