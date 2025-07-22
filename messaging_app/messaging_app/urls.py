from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),
    # Enables Login/logout for DRF's browsable API
    path('api-auth/', include('rest_framework.urls')),
]
