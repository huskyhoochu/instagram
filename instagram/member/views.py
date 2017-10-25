from pprint import pprint
from typing import NamedTuple

import requests
from django.contrib.auth import (
    get_user_model,
    login as django_login,
    logout as django_logout
)
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from config import settings
from member.decorators import login_required
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


@login_required
def profile(request):
    return HttpResponse('hello')


def facebook_login(request):
    # print(request.GET)
    # print(request.POST)
    # get_string = '<br'.join(['{}: {}'.format(key, value) for key, value in request.GET.items()])
    # post_string = '<br'.join(['{}: {}'.format(key, value) for key, value in request.POST.items()])
    # 자료구조 정의
    class AccessTokenInfo(NamedTuple):
        access_token: str
        token_type: str
        expires_in: str

    class DebugTokenInfo(NamedTuple):
        app_id: str
        application: str
        expires_at: int
        is_valid: bool
        issued_at: int
        scopes: list
        type: str
        user_id: str

    class UserInfo:
        def __init__(self, data):
            self.id = data['id']
            self.email = data.get('email', '')
            self.url_picture = data['picture']['data']['url']

    app_id = settings.FACEBOOK_APP_ID
    app_secret = settings.FACEBOOK_APP_SECRET_CODE
    app_access_token = f'{app_id}|{app_secret}'
    code_parameter = request.GET.get('code')

    # 액세스 토큰 받기
    def get_access_token_info(code):
        redirect_uri = '{scheme}://{host}{relative_url}'.format(
            scheme=request.scheme,
            host=request.META['HTTP_HOST'],
            relative_url=reverse('member:facebook_login')
        )

        url_access_token = 'https://graph.facebook.com/v2.10/oauth/access_token?'

        params_access_token = {
            'client_id': app_id,
            'redirect_uri': redirect_uri,
            'client_secret': app_secret,
            'code': code
        }

        response = requests.get(url_access_token, params_access_token)

        return AccessTokenInfo(**response.json())

    # 디버그 토큰 받기
    def get_debug_token_info(token):
        url_debug_token = 'https://graph.facebook.com/debug_token'
        params_debug_token = {
            'input_token': token,
            'access_token': app_access_token,
        }
        response = requests.get(url_debug_token, params_debug_token)
        return DebugTokenInfo(**response.json()['data'])

    access_token_info = get_access_token_info(code_parameter)
    access_token = access_token_info.access_token
    debug_token_info = get_debug_token_info(access_token)

    # 유저 정보 가져오기

    user_info_fields = [
        'id',
        'name',
        'picture',
        'email',
    ]
    url_graph_user_info = 'https://graph.facebook.com/me'
    params_graph_user_info = {
        'fields': ','.join(user_info_fields),
        'access_token': access_token,
    }
    response = requests.get(url_graph_user_info, params_graph_user_info)
    result = response.json()

    # 회원 정보 만들기

    user_info = UserInfo(data=result)

    username = f'fb_{user_info.id}'
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
    else:
        user = User.objects.create_user(
            user_type=User.USER_TYPE_FACEBOOK,
            username=username,
            age=0
        )
    django_login(request, user)
    return redirect('post:post_list')
