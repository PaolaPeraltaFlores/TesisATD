from django.contrib import admin
from django.urls import include, path
from ATD.views import handleMultipleImagesUpload
import debug_toolbar
from  django.views.decorators.csrf import csrf_exempt
from django.conf import settings

urlpatterns = [
    path('upload/', handleMultipleImagesUpload, name="home"),
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls'))
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

