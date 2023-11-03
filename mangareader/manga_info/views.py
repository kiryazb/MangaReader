from django.shortcuts import render

from django.views import generic

from .models import Work


class MangaDetailView(generic.DetailView):
    slug_field = 'title'
    model = Work
    template_name = "manga_info/manga_info.html"

