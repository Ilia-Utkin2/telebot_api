from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date')
    list_filter = ('author', 'pub_date')
    search_fields = ('title', 'text')
    readonly_fields = ('pub_date',)
    list_per_page = 25
