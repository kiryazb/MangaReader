from django.http import Http404
from django.shortcuts import render, get_object_or_404

from django.views import generic

from .models import Work, Chapter


class MangaDetailView(generic.DetailView):
    model = Work

    def get_template_names(self):
        section = self.request.GET.get('section', 'info')
        if section == 'info':
            return 'manga_info/manga_info.html'
        if section == 'chapters':
            return 'manga_info/chapters.html'


def chapter(request, slug, pk):
    work = get_object_or_404(Work, slug=slug)
    chapter = Chapter.objects.filter(work=work, chapter=pk)
    page = request.GET.get('page', '1')
    if chapter is not None:
        return render(request, 'manga_info/chapter.html', {'chapter': chapter})
    else:
        raise Http404('Chapter does not exist')
