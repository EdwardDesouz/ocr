from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from ocrapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.upload_file, name='upload_file'),
    path('download/<str:filename>/', views.download_file, name='download_file'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
