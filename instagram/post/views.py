from django.core.exceptions import PermissionDenied
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
    """
    1. 이 뷰에 접근할 때 해당 사용자가 인증된 상태가 아니면 로그인 뷰로 redirect
    2. form.is_valid()를 통과한 후 생성되는 Post 객체에 author 정보 추가
    :param request:
    :return:
    """
    # user가 유효한지 검증하는 과정
    if not request.user.is_authenticated:
        # 유저 검증을 통과하지 못하면 로그인 사이트로 리다이렉트
        return redirect('member:login')

    # post 요청 시 판정
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # 이 포스트에 정확한 데이터가 들어있다면 (유효성 검증)
            # post = Post.objects.create(
            #     author=request.user,
            #     photo=form.cleaned_data['photo']
            # )
            # post.save()
            post = form.save(commit=False)
            post.author = request.user
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
    # user가 유효한지 검증하는 과정
    if not request.user.is_authenticated:
        # 유저 검증을 통과하지 못하면 로그인 사이트로 리다이렉트
        return redirect('member:login')

    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            # 포스트와 댓글을 연결
            comment.post = post
            comment.save()
            # PostComment.objects.create(
            #     post=post,
            #     author=request.user,
            #     content=form.cleaned_data['text']
            # )
    # 생성 후 Post의 detail 화면으로 이동
    next = request.GET.get('next', '').strip()
    if next:
        return redirect(next)
    return redirect('post:post_detail', pk=pk)


def post_delete(request, pk):
    if request.method == 'POST':
        # 해당하는 포스트가 있는지 검사
        post = get_object_or_404(Post, pk=pk)
        # request.user가 Post의 author인지 검사
        if post.author == request.user:
            post.photo.delete()
            post.delete()
            return redirect('post:post_list')

        else:
            raise PermissionDenied


def comment_delete(request, pk):
    if not request.user.is_authenticated:
        return redirect('member:login')

    if request.method == 'POST':
        comment = PostComment.objects.get(pk=pk)
        post_pk = comment.post.pk
        comment.delete()

    next = request.GET.get('next')
    if next:
        return redirect(next)
    return redirect('post:post_detail', pk=post_pk)




