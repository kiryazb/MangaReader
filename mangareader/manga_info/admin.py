from django.contrib import admin

from .models import Type, Author, Imprint, Work, Chapter, Comment, CommentWorkMainPage

from django.contrib.auth.models import Permission

admin.site.register(Type)
admin.site.register(Imprint)
admin.site.register(Permission)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'work', 'chapter', 'page')


@admin.register(CommentWorkMainPage)
class CommentWorkMainPageAdmin(admin.ModelAdmin):
    list_display = ('text', 'work')


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('title', 'work', 'chapter')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'subscribers')


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'type')
    prepopulated_fields = {'slug': ('title',)}
