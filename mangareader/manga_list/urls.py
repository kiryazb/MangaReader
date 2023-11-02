from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.MangaListView.as_view(), name='manga-list'),
    path('<slug:slug>', views.MangaDetailView.as_view(), name='work-detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)