from django.contrib import admin
from newspaper_app.models import Category,Contact, Tag, Post, Comment

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(Comment)
