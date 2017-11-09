import filecmp
from pprint import pprint
from random import randint

import io

import os

import requests
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APIRequestFactory, APILiveServerTestCase

from config import settings
from post.apis import PostList
from post.models import Post

User = get_user_model()


class PostListViewTest(APILiveServerTestCase):
    URL_API_POST_LIST_NAME = 'api-posts'
    URL_API_POST_LIST = '/api/posts/'
    VIEW_CLASS = PostList

    @staticmethod
    def create_user(username='dummy'):
        return User.objects.create_user(username='dummy', age=0, password=1234)

    @staticmethod
    def create_post(author=None):
        return Post.objects.create(author=author, photo=File(io.BytesIO()))

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
        user = self.create_user()
        # 0 이상 20 이하의 임의의 숫자 지정
        num = randint(0, 20)
        # num 갯수만큼 Post 생성
        for i in range(num):
            self.create_post(author=user)

        url = reverse(self.URL_API_POST_LIST_NAME)
        # post_list에 GET 요청
        response = self.client.get(url)
        # status code가 200인지 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # objects.count 결과가 num과 같은지 확인
        self.assertEqual(Post.objects.count(), num)
        # response로 돌아온 JSON의 길이가 num과 같은지 확인
        self.assertEqual(len(response.data), num)

    def test_get_post_list_exclude_author_is_none(self):
        """
        author가 None인 Post가 PostList get 요청에서 제외되는지 테스트
        :return:
        """
        user = self.create_user()
        num_author_none_posts = randint(1, 10)
        num_posts = randint(11, 20)
        for i in range(num_author_none_posts):
            self.create_post()
        for i in range(num_posts):
            self.create_post(author=user)

        response = self.client.get(self.URL_API_POST_LIST)
        # author가 없는 Post 개수는 response에 포함되지 않는지 확인
        self.assertEqual(len(response.data), num_posts)

    def test_post_create(self):
        # 테스트용 유저 생성
        user = self.create_user()
        # 햐당 유저를 현재 client에 강제로 인증
        self.client.force_authenticate(user=user)
        # 테스트용 이미지 파일의 경로
        path = os.path.join(settings.STATIC_DIR, 'images', 'olivier_tallec.png')
        print('파일 경로 : ', path)

        # path에서 받은 파일을 post 요청에 photo 값으로 전달
        with open(path, 'rb') as photo:
            response = self.client.post(self.URL_API_POST_LIST, {
                'photo': photo,
            })

        # response code가 201인지 확인
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print('응답 코드 : ', response.status_code)
        # 생성된 객체가 1개가 맞는지 확인
        self.assertEqual(Post.objects.count(), 1)
        print('생성된 객체 갯수 : ', Post.objects.count())
        # 업로드를 시도한 파일과 실제 올라간 파일이 같은지 확인
        # 바이너리 구조가 같은지를 비교
        # 파이썬에 모듈이 있다
        post = Post.objects.get(pk=response.data['pk'])
        print('업로드한 파일 : ', path)

        if settings.STATICFILES_STORAGE == 'django.contrib.staticfiles.Static':
            # 파일시스템에서 두 파일 비교
            self.assertTrue(filecmp.cmp(path, post.photo.file.url))

        else:
            # S3에서 비교
            url = post.photo.url
            print('S3 경로 :', url)
            response = requests.get(url)
            print('응답 결과 : ', response)
            # 장고에서 임시 파일을 생성, 확장자를 설정하고 with문이 닫혀도 파일이 삭제되지 않도록 delete=False 옵션을 준다
            with NamedTemporaryFile(suffix='png', delete=False) as temp_file:
                # 응답 결과 response의 컨텐츠를 파일로 작성한다
                temp_file.write(response.content)
            print('파일 이름 : ', temp_file.name)
            self.assertTrue(filecmp.cmp(path, temp_file.name))

        # login = self.client.force_authenticate(user=user)
        # print('로그인 결과 : ', login)
        # response = self.client.post(self.URL_API_POST_LIST, {'photo': File(io.BytesIO())})
        # print('응답 결과 : ', response)
        # # response2 = self.client.post(response, {'id': 'dummy', 'password': '1234'})
        # # # response = self.client.get(create)
        # # print(response2)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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
