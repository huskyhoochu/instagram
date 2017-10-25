from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from member.forms import SignupForm
from .models import User


# 유저 어드민 커스텀
class UserAdmin(BaseUserAdmin):
    # 유저 보기에서 필드셋 추가
    fieldsets = BaseUserAdmin.fieldsets + (
        ('추가 정보', {'fields': (
            'img_profile',
            'age',
            'user_type',
            'like_posts',
        )}),
    )
    # 유저 가입에서 필드셋 추가
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('추가 정보', {
            'fields': (
                'img_profile',
                'age',
                'user_type',
            )
        }),
    )

    add_form = SignupForm


admin.site.register(User, UserAdmin)
