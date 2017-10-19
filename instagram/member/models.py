from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager
)
from django.db import models


# 프록시 모델에서 사용했던 프록시 모델 매니저
class UserManager(DjangoUserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(age=30, *args, **kwargs)


class User(AbstractUser):
    img_profile = models.ImageField(upload_to='user', blank=True)
    age = models.IntegerField()

    objects = UserManager()

    # REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ['age']
