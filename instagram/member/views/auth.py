from django.contrib.auth import (
    get_user_model,
    login as django_login,
    logout as django_logout
)
from django.shortcuts import render, redirect

from config import settings
from ..forms import SignupForm, LoginForm

User = get_user_model()

__all__ = (
    'login',
    'logout',
    'signup',
)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return redirect('post:post_list')
    else:
        form = LoginForm()
    context = {
        'login_form': form,
        'facebook_app_id': settings.FACEBOOK_APP_ID,
        'fb_scope': settings.FACEBOOK_SCOPE,
    }
    next_path = request.GET.get('next')
    if next_path:
        return redirect(next_path)
    return render(request, 'member/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('post:post_list')


def signup(request):
    if request.method == 'POST':
        # 이미지 프로필을 업로드했을 경우
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            django_login(request, user)
            return redirect('post:post_list')

    # GET 요청 시
    else:
        form = SignupForm()
    context = {
        'signup_form': form
    }
    return render(request, 'member/signup.html', context)
