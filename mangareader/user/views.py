from django.http import Http404
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm, AddAuthorForm, ChangeAuthorForm

from django.views import generic

from django.contrib.auth import authenticate, login, logout

from .models import CustomUser
from manga_info.models import Author


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            CustomUser.objects.create_user(username=username, password=password)
            return redirect('/home/')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/home/')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def custom_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/home/')


class UserDetailView(generic.DetailView):
    slug_field = 'username'
    model = CustomUser

    def get_template_names(self):
        user = self.request.user
        group_names = user.groups.values_list('name', flat=True)
        if 'Moderator' in group_names:
            return 'user/moderator_profile.html'
        return "user/profile.html"


def moderator_panel(request, slug):
    return render(request, 'user/moderator_panel.html')


def moderator_author(request, slug):
    return render(request, 'user/moderator_author.html')


def add_author(request, slug):
    authors = Author.objects.all()
    is_exist = 0
    if request.method == 'POST':
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            author_name = form.cleaned_data['first_name']
            author_last = form.cleaned_data['last_name']
            authors_exist = Author.objects.filter(first_name__icontains=author_name,
                                                  last_name__icontains=author_last).exists()
            if not authors_exist:
                is_exist = 1
                form.save()
            else:
                is_exist = -1
    else:
        form = AddAuthorForm()
    return render(request, 'user/add_author.html', {'form': form, 'is_exist': is_exist})


def change_author(request, slug):
    authors = Author.objects.all()
    is_exist = 0
    if request.method == 'POST':
        form = ChangeAuthorForm(request.POST)
        print('------------------')
        if form.is_valid():
            author_old_name = form.cleaned_data['old_name']
            author_old_last = form.cleaned_data['old_last']
            print(f'---------------------------{author_old_name}-------{author_old_last}')
            author_name = form.cleaned_data['first_name']
            author_last = form.cleaned_data['last_name']
            author_subscribers = form.cleaned_data['subscribers']
            authors_exist = Author.objects.filter(first_name__icontains=author_old_name,
                                                  last_name__icontains=author_old_last).exists()
            if authors_exist:
                is_exist = 1
                Author.objects.filter(first_name=author_old_name,
                                      last_name=author_old_last).update(first_name=author_name, last_name=author_last,
                                                                        subscribers=author_subscribers)
            else:
                is_exist = -1
    else:
        form = ChangeAuthorForm()
    return render(request, 'user/change_author.html', {'form': form, 'is_exist': is_exist})
