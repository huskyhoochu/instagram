from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework.test import APITestCase

from ... import views


class PostLikeToggleViewTest(TestCase):
    TEST_POST_PK = 1
    VIEW_URL = '/post/1/like-toggle/'
    VIEW_URL_NAME = 'post:post_like_toggle'

    def test_url_equal_reverse_url_name(self):
        """
        VIEW_URL_NAME을 reverse해서 만든 URL이
        VIEW_URL과 같은지 테스트
        :return:
        """
        self.assertEqual(
            self.VIEW_URL,
            reverse(self.VIEW_URL_NAME, kwargs={
                'pk': self.TEST_POST_PK}))

    def test_url_resolves_to_post_like_toggle_view(self):
        found = resolve(self.VIEW_URL)
        self.assertEqual(found.func, views.post_like_toggle)


