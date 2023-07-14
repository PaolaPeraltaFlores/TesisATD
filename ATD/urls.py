from django.contrib import admin
from django.urls import include, path
from ATD.views import  UploadImageCreate,ImageList,ImagebyID,ImagebyIDcolordominante
from  django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .routers import router
urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('upload-second/', UploadImageCreate.as_view(), name="user_upload_image"),
    path('list-images/', ImageList.as_view(), name="user_list_image"),
    path('image-by-ID/<pk>', ImagebyID.as_view(), name="user_ImageID"),
    path('color-by-ID/<pk>', ImagebyIDcolordominante.as_view(), name="user_colordominante")
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

