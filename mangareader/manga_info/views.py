import os

from django.http import Http404
from django.shortcuts import render, get_object_or_404

from django.views import generic

from .models import Work, Chapter

from zipfile import ZipFile


class MangaDetailView(generic.DetailView):
    model = Work

    def get_template_names(self):
        section = self.request.GET.get('section', 'info')
        if section == 'info':
            return 'manga_info/manga_info.html'
        if section == 'chapters':
            return 'manga_info/chapters.html'


# def chapter(request, slug, pk):
#     work = get_object_or_404(Work, slug=slug)
#     chapter = Chapter.objects.filter(work=work, chapter=pk)
#     page = request.GET.get('page', '1')
#     print(Chapter.image)
#     # if chapter is not None:
#     #     return render(request, 'manga_info/chapter.html', {'chapter': chapter})
#     # else:
#     #     raise Http404('Chapter does not exist')


def chapter(request, slug, pk):
    work = get_object_or_404(Work, slug=slug)
    chapter = Chapter.objects.filter(work=work, chapter=pk)[0]
    page = request.GET.get('page', '1')

    zip_file_path = chapter.image.path
    temp_extracted_dir = '\\'.join(zip_file_path.split('\\')[:-1])

    if os.path.exists(zip_file_path):

        with ZipFile(zip_file_path, "r") as myzip:
            myzip.extractall(temp_extracted_dir)

        os.remove(zip_file_path)

        image_files = os.listdir(temp_extracted_dir)

        files_name = []

        count = 1
        for old_name in image_files:
            name, extension = old_name.split('.')
            new_name = f'{count}.{extension}'

            old_path = os.path.join(temp_extracted_dir, old_name)
            new_path = os.path.join(temp_extracted_dir, new_name)

            os.rename(old_path, new_path)

            files_name.append(new_name)

            count += 1

    else:
        files_name = []
        for files in os.listdir(temp_extracted_dir):
            files_name.append(files)

    if chapter is not None:
        index = temp_extracted_dir.split('\\').index('media')
        page_count = len(files_name)
        image_url = '/' + '\\'.join(temp_extracted_dir.split('\\')[index:]).replace('\\', '/') + '/' + files_name[
            int(page) - 1]
        return render(request, 'manga_info/chapter.html', {'url': image_url, 'page': str(int(page) + 1),
                                                           'current_page': int(page),
                                                           'work': work, 'chapter': chapter,
                                                           'page_count': page_count})
    else:
        raise Http404('Chapter does not exist')
