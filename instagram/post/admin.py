from django.contrib import admin

from post.models import Post, PostComment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'created_at']
    list_display_links = ['content']


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'created_at']
    list_display_links = ['id']
