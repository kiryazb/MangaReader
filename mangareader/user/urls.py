from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('<slug:slug>/moderator/', views.moderator_panel, name='moderator-panel'),
    path('<slug:slug>', views.UserDetailView.as_view(), name='profile'),
    path('<slug:slug>/moderator/author_panel/', views.moderator_author, name='moderator_author'),
    path('<slug:slug>/moderator/author_panel/add_author/', views.add_author, name='add_author'),
    path('<slug:slug>/moderator/author_panel/change_author/', views.change_author, name='change_author')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)