from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('communitydetection/', include('cd_app.urls')),
]
