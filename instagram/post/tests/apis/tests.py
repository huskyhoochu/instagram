from pprint import pprint
from random import randint

import io

from django.contrib.auth import get_user_model
from django.core.files import File
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APIRequestFactory, APILiveServerTestCase

from post.apis import PostList
from post.models import Post

User = get_user_model()


class PostListViewTest(APILiveServerTestCase):
    URL_API_POST_LIST_NAME = 'api-posts'
    URL_API_POST_LIST = '/api/posts/'
    VIEW_CLASS = PostList

    def test_post_list_url_name_reverse(self):
        url = reverse(self.URL_API_POST_LIST_NAME)
        print('reverse test(url):', url)
        self.assertEqual(url, self.URL_API_POST_LIST)

    def test_post_list_url_resolve_view_class(self):
        # /api/posts/에 매칭되는 ResolverMatch 객체를 가져옴
        resolve_match = resolve(self.URL_API_POST_LIST)
        # ResolverMatch의 url_name이 'api-post'인지 확인
        self.assertEqual(resolve_match.url_name, self.URL_API_POST_LIST_NAME)
        # ResolverMatch의 func이 PostList인지 확인
        self.assertEqual(resolve_match.func.view_class, self.VIEW_CLASS.as_view().view_class)

    def test_get_post_list(self):
        # 유저 지정
        user = User.objects.create_user(username='dummy', age=0)
        # 0 이상 20 이하의 임의의 숫자 지정
        num = randint(0, 20)
        # num 갯수만큼 Post 생성
        for i in range(num):
            Post.objects.create(
                author=user,
                photo=File(io.BytesIO())
            )

        url = reverse(self.URL_API_POST_LIST_NAME)
        # post_list에 GET 요청
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # objects.count 결과가 num과 같은지 확인
        self.assertEqual(Post.objects.count(), num)
        # response로 돌아온 JSON의 길이가 num과 같은지 확인
        self.assertEqual(len(response.data), num)


# # Request 객체를 생성
# factory = APIRequestFactory()
# request = factory.get('/api/posts/')
# print(request)
#
# # PostList.as_view()로 생성한 뷰 함수를 'view' 변수에 할당
# view = PostList.as_view()
# # view 함수에 request를 전달
# response = view(request)
#
# # 결과는 JSON 데이터
# pprint(response.data)
