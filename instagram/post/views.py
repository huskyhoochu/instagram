from django.shortcuts import render, redirect

from post.models import Post, PostComment
from .forms import UploadFileForm


def post_list(request):
    if request.method=='POST':
        comment = PostComment.objects.create(
            content=request.POST.get('comment')
        )
        comment.save()
        return redirect('post_list')

    else:
        posts = Post.objects.order_by('-created_at')
        context = {
            'posts': posts
        }
        return render(request, 'post/post_list.html', context)


def post_add(request):
    if request.method=="POST":
        post = Post.objects.create(
            photo=request.FILES.get('photo'),
            content=request.POST.get('content')
        )
        post.save()
        return redirect('post_list')
    else:
        return render(request, 'post/post_form.html')

