from django.contrib import admin
from blog.models import Blog, Story

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')

admin.site.register(Blog, BlogAdmin)
admin.site.register(Story)
