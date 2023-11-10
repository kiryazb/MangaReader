from django.shortcuts import render

from django.views import generic

from manga_info.models import Work


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        work_type = self.request.GET.get('type', '1')
        if work_type == '1':
            context['type'] = "Manga"
        elif work_type == '2':
            context['type'] = "Manhwa"
        return context

    def get_queryset(self):
        return Work.objects.order_by('title')
