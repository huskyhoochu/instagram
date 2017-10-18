from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from member.forms import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['id'],
                password=form.cleaned_data['password']
            )
            return HttpResponse(f'{user.username}, {user.password}')


    return render(request, 'member/signup.html')
