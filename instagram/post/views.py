from django.shortcuts import render, redirect, get_object_or_404

from post.models import Post, PostComment
from .forms import PostForm, PostCommentForm


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
    comment_form = PostCommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_list.html', context)


def post_add(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # 이 포스트에 정확한 데이터가 들어있다면 (유효성 검증)
            post = Post.objects.create(
                photo=form.cleaned_data['photo']
            )
            post.save()
            return redirect('post_list')

    else:
        # GET 요청의 경우 빈 PostForm 인스턴스를 생성해 탬플릿에 전달
        form = PostForm()

    # GET 요청에선 이 부분이 무조건 실행됨
    # POST 요청에선 form.is_vaild()를 통과하지 못하면 이 부분이 실행됨
    return render(request, 'post/post_form.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post
    }
    return render(request, 'post/post_detail.html', context)


def comment_add(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostCommentForm(request.POST)
        if form.is_valid():
            PostComment.objects.create(
                post=post,
                content=form.cleaned_data['text']
            )
            return redirect('post_list')

    else:
        form = PostCommentForm()

    context = {
        'form': form,
    }

    return render(request, 'post/post_list.html', context)