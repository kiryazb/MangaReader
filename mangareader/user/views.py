from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm

from django.views import generic

from django.contrib.auth import authenticate, login, logout

from .models import CustomUser


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
    template_name = "user/profile.html"
