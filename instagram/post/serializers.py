from rest_framework import serializers

from member.serializers import UserSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    # author를 pk값이 아닌 user 객체로 올 수 있도록 세팅
    author = UserSerializer()

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'photo',
            'created_at',
        )
