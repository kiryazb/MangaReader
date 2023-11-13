from django.contrib import admin

from .models import Type, Author, Imprint, Work, Chapter, Comment

admin.site.register(Type)
admin.site.register(Imprint)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'work', 'chapter', 'page')


class ChapterAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Chapter, ChapterAdmin)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'subscribers')


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'type')
    prepopulated_fields = {'slug': ('title',)}
