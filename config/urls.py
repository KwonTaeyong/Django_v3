from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, re_path, include
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.conf import settings

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


urlpatterns = [
                  path('', lambda request: redirect('swagger/', permanent=True)),
                  path('admin/', admin.site.urls),
                  path('gongo/', include('gongo.urls')),
                  path('bbs/', include('bbs.urls')),
                  path('common/', include('common.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

schema_view = get_schema_view(
    openapi.Info(
        title="8125 API",
        default_version="v240320",
        description='''
            API documentation for 8125
        ''',
        # terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="mmr@nowonlab.com"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns += [
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]


