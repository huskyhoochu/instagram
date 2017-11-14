from django.shortcuts import render

from ..forms import User


def profile(request, pk):
    user = User.objects.get(pk=pk)

    context = {
        'user': user
    }

    return render(request, 'member/profile.html', context)
