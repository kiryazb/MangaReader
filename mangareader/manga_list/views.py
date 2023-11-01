from django.shortcuts import render

from django.views import generic

from .models import Work


class MangaListView(generic.ListView):
    template_name = "manga_list/manga_list.html"
    model = Work
    paginate_by = 10

    def get_template_names(self):
        work_type = self.request.GET.get('type', '1')
        if work_type == '1':
            return ["manga_list/manga_list.html"]
        elif work_type == '2':
            return ["manga_list/manhwa_list.html"]
