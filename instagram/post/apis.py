from django.http import Http404

from rest_framework import status, mixins, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializers import UserSerializer
from post.pagination import StandardPostViewPagination
from post.serializers import PostSerializer
from .models import Post
from utils.permissions import IsAuthorOrReadOnly


class PostList(generics.ListCreateAPIView):
    # generics.GenericAPIView와 mixins를 상속받아 처리
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = StandardPostViewPagination
    # permission_classes = (
    #     permissions.IsAuthenticated,
    # )
    #
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)
    #
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def get(self, request):
    #     posts = Post.objects.all()
    #     serializer = PostSerializer(posts, many=True)
    #     return Response(serializer.data)
    #
    # def post(self, request):
    #     serializer = PostSerializer(data=request.data)
    #     if serializer.is_valid():
    #         # 포스트맨에서 파일 올릴 때 author가 생긴다
    #         serializer.save(author=self.request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PostDetail(APIView):
#     def get_object(self, post_pk):
#         try:
#             return Post.objects.get(pk=post_pk)
#         except Post.DoesNotExist:
#             raise Http404
#
#     def get(self, request, post_pk):
#         post = self.get_object(post_pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#
#     def delete(self, request, post_pk):
#         post = self.get_object(post_pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class PostDetail(generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsAuthorOrReadOnly,
    )


class PostLikeToggle(generics.GenericAPIView):
    queryset = Post.objects.all()
    lookup_url_kwarg = 'post_pk'

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        # 이미 유저의 like_posts 목록에 현재 post(instance)가 존재할 경우
        if user.like_posts.filter(pk=instance.pk):
            user.like_posts.remove(instance)
            like_status = False
        else:
            user.like_posts.add(instance)
            like_status = True
        data = {
            'user': UserSerializer(user).data,
            'post': PostSerializer(instance).data,
            'result': like_status,

        }
        return Response(data)
