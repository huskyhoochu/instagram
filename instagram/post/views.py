from django.shortcuts import render, redirect

from post.models import Post, PostComment
from .forms import PostForm


def post_list(request):
    # if request.method == 'POST':
    #     comment = PostComment.objects.create(
    #
    #         content=request.POST.get('comment')
    #     )
    #     comment.save()
    #     return redirect('post_list')
    #
    # elif request.method == 'GET':
    posts = Post.objects.order_by('-created_at')
    context = {
        'posts': posts
    }
    return render(request, 'post/post_list.html', context)


def post_add(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # 이 포스트에 정확한 데이터가 들어있다면 (유효성 검증)
            post = Post.objects.create(
                photo=form.cleaned_data['photo'],
                content=request.POST.get('content')
            )
            post.save()
            return redirect('post_list')

    else:
        form = PostForm()

    return render(request, 'post/post_form.html', {'form': form})

