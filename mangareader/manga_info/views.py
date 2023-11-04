from django.shortcuts import render

from django.views import generic

from .models import Work


class MangaDetailView(generic.DetailView):
    slug_field = 'title'
    model = Work

    def get_template_names(self):
        section = self.request.GET.get('section', 'info')
        if section == 'info':
            return 'manga_info/manga_info.html'
        if section == 'chapters':
            return 'manga_info/chapters.html'



