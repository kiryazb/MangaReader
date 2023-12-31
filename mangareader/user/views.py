from django.contrib.auth.decorators import user_passes_test
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, LoginForm, AddAuthorForm, ChangeAuthorForm, DeleteAuthorForm, AddChapterForm, \
    ChangeChapterForm, DeleteChapterForm

from django.views import generic

from django.contrib.auth import authenticate, login, logout

from .models import CustomUser
from manga_info.models import Author, Chapter, Work


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


def is_moderator(user):
    print()
    return user.groups.filter(name='Moderator').exists()


@user_passes_test(is_moderator, login_url='/home/')
def moderator_panel(request, slug):
    return render(request, 'user/moderator_panel.html')


@user_passes_test(is_moderator, login_url='/home/')
def moderator_author(request, slug):
    return render(request, 'user/moderator_author.html')


@user_passes_test(is_moderator, login_url='/home/')
def add_author(request, slug):
    authors = Author.objects.all()
    is_exist = 0
    if request.method == 'POST':
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            author_name = form.cleaned_data['first_name']
            author_last = form.cleaned_data['last_name']
            authors_exist = Author.objects.filter(first_name=author_name,
                                                  last_name=author_last).exists()
            if not authors_exist:
                is_exist = 1
                form.save()
            else:
                is_exist = -1
    else:
        form = AddAuthorForm()
    return render(request, 'user/add_author.html', {'form': form, 'is_exist': is_exist})


@user_passes_test(is_moderator, login_url='/home/')
def change_author(request, slug):
    authors = Author.objects.all()
    is_exist = 0
    if request.method == 'POST':
        form = ChangeAuthorForm(request.POST)
        if form.is_valid():
            author_old_name = form.cleaned_data['old_name']
            author_old_last = form.cleaned_data['old_last']
            author_name = form.cleaned_data['first_name']
            author_last = form.cleaned_data['last_name']
            author_subscribers = form.cleaned_data['subscribers']
            authors_exist = Author.objects.filter(first_name=author_old_name,
                                                  last_name=author_old_last).exists()
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


@user_passes_test(is_moderator, login_url='/home/')
def delete_author(request, slug):
    authors = Author.objects.all()
    is_exist = 0
    if request.method == 'POST':
        form = DeleteAuthorForm(request.POST)
        if form.is_valid():
            author_name = form.cleaned_data['first_name']
            author_last = form.cleaned_data['last_name']
            authors_exist = Author.objects.filter(first_name=author_name,
                                                  last_name=author_last).exists()
            if authors_exist:
                is_exist = 1
                Author.objects.filter(first_name=author_name,
                                      last_name=author_last).delete()
            else:
                is_exist = -1
    else:
        form = DeleteAuthorForm()

    return render(request, 'user/delete_author.html', {'form': form, 'is_exist': is_exist})


@user_passes_test(is_moderator, login_url='/home/')
def moderator_chapter(request, slug):
    return render(request, 'user/moderator_chapter.html')


def manga_updates(request, work, chapter, slug):
    manga_updates = request.session.get('manga_updates', [''] * 5)
    last_pos = request.session.get('last_pos', 0)
    manga_updates[last_pos] = (work, chapter, slug)
    request.session['manga_updates'] = manga_updates
    if last_pos + 1 < 5:
        request.session['last_pos'] = last_pos + 1
    else:
        request.session['last_pos'] = 0


@user_passes_test(is_moderator, login_url='/home/')
def add_chapter(request, slug):
    chapters = Chapter.objects.all()
    is_exist = 0
    if request.method == 'POST':
        form = AddChapterForm(request.POST, request.FILES)
        if form.is_valid():

            chapter_title = form.cleaned_data['title']
            chapter_work = form.cleaned_data['work']
            chapter_chapter = form.cleaned_data['chapter']
            chapters_exist = Chapter.objects.filter(title=chapter_title, work=chapter_work).exists()
            if not chapters_exist:
                is_exist = 1
                manga_updates(request, chapter_work.title, chapter_chapter, chapter_work.slug)
                print(f'-------------{request.session["manga_updates"]}')
                form.save()
            else:
                is_exist = -1
    else:
        form = AddChapterForm()
    return render(request, 'user/add_chapter.html', {'form': form, 'is_exist': is_exist})


@user_passes_test(is_moderator, login_url='/home/')
def change_chapter(request, slug):
    chapters = Chapter.objects.all()
    is_exist = 0
    if request.method == 'POST':
        form = ChangeChapterForm(request.POST, request.FILES)
        if form.is_valid():
            chapter_old_title = form.cleaned_data['old_title']
            chapter_old_work = form.cleaned_data['work']
            chapter_title = form.cleaned_data['title']
            chapter_work = form.cleaned_data['work']
            chapter_chapter = form.cleaned_data['chapter']
            chapter_image = form.cleaned_data['image']
            chapters_exist = Chapter.objects.filter(title=chapter_old_title,
                                                    work=chapter_old_work).exists()
            if chapters_exist:
                is_exist = 1
                Chapter.objects.filter(title=chapter_old_title,
                                       work=chapter_old_work).update(title=chapter_title, work=chapter_work)

                chapter_instance = Chapter.objects.get(title=chapter_title, work=chapter_work)
                chapter_instance.image.delete()
                chapter_instance.image.save(chapter_image.name, chapter_image, save=True)
            else:
                is_exist = -1
    else:
        form = ChangeChapterForm()
    return render(request, 'user/change_chapter.html', {'form': form, 'is_exist': is_exist})


@user_passes_test(is_moderator, login_url='/home/')
def delete_chapter(request, slug):
    chapters = Chapter.objects.all()
    is_exist = 0
    if request.method == 'POST':
        form = DeleteChapterForm(request.POST, request.FILES)
        if form.is_valid():
            chapter_title = form.cleaned_data['title']
            chapter_work = form.cleaned_data['work']
            chapters_exist = Chapter.objects.filter(title=chapter_title, work=chapter_work).exists()
            if chapters_exist:
                is_exist = 1
                Chapter.objects.filter(title=chapter_title,
                                       work=chapter_work).delete()
            else:
                is_exist = -1
    else:
        form = DeleteChapterForm()
    return render(request, 'user/delete_chapter.html', {'form': form, 'is_exist': is_exist})
