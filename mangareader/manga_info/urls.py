from django.contrib import admin
from django.urls import path, include

from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static

from .import views


urlpatterns = [
    path('', views.MangaDetailView.as_view(), name='work-detail'),
    path('c<int:pk>/', views.chapter, name='chapter-detail')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
