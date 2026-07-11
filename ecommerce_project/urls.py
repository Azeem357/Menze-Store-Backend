# your_project/urls.py  (the root urls.py, not the app one)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('store.urls')),   # ← rename 'store' to your app name
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

