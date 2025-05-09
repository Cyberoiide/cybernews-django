from django.contrib import admin # type: ignore
from .models import Article, Source, Vote, Comment

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'score', 'created_at')
    search_fields = ('title', 'tags', 'content')
    list_filter = ('source', 'created_at')
    ordering = ('-created_at',)

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain')
    search_fields = ('name',)

admin.site.register(Vote)
admin.site.register(Comment)
