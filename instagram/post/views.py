from django.shortcuts import render, redirect, get_object_or_404
from post.models import Post, PostComment
from .forms import PostForm, PostCommentForm


def post_list(request):
    # 작가가 없으면 떠오르지 않도록 막기
    posts = Post.objects.all()
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
            return redirect('post:post_list')

    else:
        # GET 요청의 경우 빈 PostForm 인스턴스를 생성해 탬플릿에 전달
        form = PostForm()

    # GET 요청에선 이 부분이 무조건 실행됨
    # POST 요청에선 form.is_vaild()를 통과하지 못하면 이 부분이 실행됨
    return render(request, 'post/post_form.html', {'form': form})


def post_detail(request, pk):
    # get_object_or_404는 쿼리셋을 받을 수 있다
    post = get_object_or_404(Post, pk=pk)
    comment_form = PostCommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,
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

    next = request.GET.get('next')
    if next:
        return redirect(next)
    return redirect('post:post_detail', pk=pk)


def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post.photo.delete()
        post.delete()
        return redirect('post:post_list')

    else:
        return redirect('post:post_list')
