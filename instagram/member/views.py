from django.contrib.auth import get_user_model, logout as django_logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm

User = get_user_model()


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return redirect('post:post_list')
    else:
        form = LoginForm()
    context = {
        'login_form': form
    }
    return render(request, 'member/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('post:post_list')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.signup()
            return HttpResponse(f'{user.username}, {user.password}')

    else:
        form = SignupForm()
    context = {
        'signup_form': form
    }
    return render(request, 'member/signup.html', context)
