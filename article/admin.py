from django.contrib import admin
from .models import Article, Like, Comment

admin.site.register(Article)
admin.site.register(Like)
admin.site.register(Comment)