from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('<slug:slug>', views.UserDetailView.as_view(), name='profile'),
    path('<slug:slug>/moderator/', views.moderator_panel, name='moderator-panel'),
    path('<slug:slug>/moderator/author_panel/', views.moderator_author, name='moderator_author'),
    path('<slug:slug>/moderator/author_panel/add_author/', views.add_author, name='add_author'),
    path('<slug:slug>/moderator/author_panel/change_author/', views.change_author, name='change_author'),
    path('<slug:slug>/moderator/author_panel/delete_author/', views.delete_author, name='delete_author'),
    path('<slug:slug>/moderator/author_panel/delete_author/', views.delete_author, name='delete_author'),
    path('<slug:slug>/moderator/chapter_panel/', views.moderator_chapter, name='moderator_chapter'),
    path('<slug:slug>/moderator/chapter_panel/add_chapter', views.add_chapter, name='add_chapter'),
    path('<slug:slug>/moderator/chapter_panel/change_chapter', views.change_chapter, name='change_chapter'),
    path('<slug:slug>/moderator/chapter_panel/delete_chapter', views.delete_chapter, name='delete_chapter'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)