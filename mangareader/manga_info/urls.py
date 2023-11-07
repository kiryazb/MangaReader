from django.contrib import admin
from django.urls import path, include

from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static

from .import views


urlpatterns = [
    path('', views.MangaDetailView.as_view(), name='work-detail'),
    #create path to chapter
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
