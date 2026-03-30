
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lists.urls')),
    path('accounts/', include('allauth.urls')),  # маршруты для логина через Google
]
