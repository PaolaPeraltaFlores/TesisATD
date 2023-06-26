from django.contrib import admin
from django.urls import include, path
from ATD.views import UserViewSet
from  django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .routers import router
urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('upload-image/', UserViewSet.as_view(), name="user_create")
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

