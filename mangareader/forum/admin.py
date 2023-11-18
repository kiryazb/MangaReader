from django.contrib import admin

from .models import Topic, TopicComment


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'Author')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(TopicComment)
class TopicCommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'topic')
