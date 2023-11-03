from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.MangaListView.as_view(), name='manga-list'),
    path('', include("manga_info.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)