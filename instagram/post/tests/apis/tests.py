from pprint import pprint

from django.urls import reverse, resolve
from rest_framework.test import APIRequestFactory, APILiveServerTestCase

from post.apis import PostList


class PostListViewTest(APILiveServerTestCase):
    URL_API_POST_LIST_NAME = 'api-posts'
    URL_API_POST_LIST = '/api/posts/'
    VIEW_CLASS = PostList

    def test_post_list_url_name_reverse(self):
        url = reverse(self.URL_API_POST_LIST_NAME)
        print('reverse test(url):', url)
        self.assertEqual(url, self.URL_API_POST_LIST)

    def test_post_list_url_resolve_view_class(self):
        resolve_match = resolve(self.URL_API_POST_LIST)
        self.assertEqual(resolve_match.url_name, self.URL_API_POST_LIST_NAME)
        self.assertEqual(resolve_match.func.view_class, self.VIEW_CLASS.as_view().view_class)


# Request 객체를 생성
factory = APIRequestFactory()
request = factory.get('/api/posts/')
print(request)

# PostList.as_view()로 생성한 뷰 함수를 'view' 변수에 할당
view = PostList.as_view()
# view 함수에 request를 전달
response = view(request)

# 결과는 JSON 데이터
pprint(response.data)
