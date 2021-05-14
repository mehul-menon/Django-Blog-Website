from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Comment, Post
# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)


