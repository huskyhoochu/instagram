from django.shortcuts import redirect, get_object_or_404

from member.decorators import login_required
from ..models import Post, PostComment
from ..forms import PostCommentForm


@login_required
def comment_add(request, pk):
    # # user가 유효한지 검증하는 과정
    # if not request.user.is_authenticated:
    #     # 유저 검증을 통과하지 못하면 로그인 사이트로 리다이렉트
    #     return redirect('member:login')

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


@login_required
def comment_delete(request, pk):
    # if not request.user.is_authenticated:
    #     return redirect('member:login')

    if request.method == 'POST':
        comment = PostComment.objects.get(pk=pk)
        post_pk = comment.post.pk
        comment.delete()

    next = request.GET.get('next')
    if next:
        return redirect(next)
    return redirect('post:post_detail', pk=post_pk)
