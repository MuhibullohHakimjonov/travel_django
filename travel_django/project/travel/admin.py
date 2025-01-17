from django.contrib import admin
from .models import Category, Article


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'publish_date', 'category']
    list_display_links = ['id', 'title', 'publish_date', 'category']



admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
