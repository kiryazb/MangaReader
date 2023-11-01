from django.contrib import admin

from .models import Type, Author, Imprint, Work

admin.site.register(Type)
admin.site.register(Imprint)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'subscribers')


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'type')
