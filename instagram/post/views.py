from django.shortcuts import render

from post.models import Post


def post_list(request):
    posts = Post.objects.order_by('-created_at')
    context = {
        'posts': posts
    }
    return render(request, 'post/post_list.html', context)