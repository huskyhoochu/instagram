from django.contrib.auth import get_user_model, authenticate, login as django_login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm

User = get_user_model()


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return redirect('post_list')
    else:
        form = LoginForm()
    context = {
        'login_form': form
    }
    return render(request, 'member/login.html', context)


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