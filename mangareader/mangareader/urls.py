from django.contrib import admin
from django.urls import path, include

from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views

from user.views import register, custom_login, custom_logout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='home/', permanent=False)),
    path('home/', include('home.urls')),
    path('manga-list/', include('manga_list.urls')),
    path('', include('manga_info.urls')),
    path('register/', register, name='register'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
