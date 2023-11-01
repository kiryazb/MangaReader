from django.shortcuts import render

from django.views import generic

from .models import Work


def home_page(request):
    return render(request, 'home/home_page.html')


class WorkListView(generic.ListView):
    model = Work
    paginate_by = 10