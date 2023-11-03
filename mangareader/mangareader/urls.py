from django.contrib import admin
from django.urls import path, include

from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static

from user.views import register


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='home/', permanent=False)),
    path('home/', include('home.urls')),
    path('manga-list/', include('manga_list.urls')),
    path('', include('manga_info.urls')),
    path('register/', register, name='register')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
