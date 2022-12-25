from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('fileSystem/', include('fileSystem.urls')),
    path('admin/', admin.site.urls),
]
