from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager,
)
from django.db import models


# 프록시 모델에서 사용했던 프록시 모델 매니저
from rest_framework.authtoken.models import Token


class UserManager(DjangoUserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(age=30, *args, **kwargs)


class User(AbstractUser):
    # 소셜 유저 타입 정의
    USER_TYPE_FACEBOOK = 'f'
    USER_TYPE_DJANGO = 'd'
    CHOICES_USER_TYPE = (
        (USER_TYPE_FACEBOOK, 'facebook'),
        (USER_TYPE_DJANGO, 'django'),
    )
    user_type = models.CharField(max_length=1, choices=CHOICES_USER_TYPE)
    # 여러 가지 요소들
    nickname = models.CharField(max_length=50, blank=True, null=True)
    img_profile = models.ImageField(
        '프로필 이미지',
        upload_to='user',
        blank=True)
    age = models.IntegerField('나이')
    # 좋아요
    like_posts = models.ManyToManyField(
        'post.Post',
        verbose_name='좋아요 누른 포스트 목록',
        blank=True
    )
    # 내가 팔로우하고 있는 유저 목록
    #
    # 내가 A를 follow한다 == 나는 A의 follower

    following_users = models.ManyToManyField(
        'self',
        through='Relation',
        symmetrical=False,
        related_name='followers',
    )

    objects = UserManager()

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'

    # REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ['age']

    @property
    def token(self):
        return Token.objects.get_or_create(user=self)[0].key

    def follow_toggle(self, user):
        """
        1. 주어진 user가 user 객체인지 확인

        :param user:
        :return:
        """
        if not isinstance(user, User):
            raise ValueError('"user" argument must be User instance!')

        relation, relation_created = self.following_user_relations.get_or_create(to_user=user)
        if relation_created:
            return True
        relation.delete()
        return False


class Relation(models.Model):
    # User follow 목록을 가질 수 있도록
    # MTM에 대한 중개모델을 구성
    # from_user, to_user, created_at으로 3개의 필드를 사용
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following_user_relations'
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower_relations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Relation (' \
               f'from: {self.from_user.username}, ' \
               f'to: {self.to_user.username})'
