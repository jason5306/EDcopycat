import imp
from django.contrib import admin
from .models import Post, Category, Profile, Comment,Course
# Register your models here.

# show POST section in Site adminstration page
admin.site.register(Post) 
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Course)

class CommentAdmin(admin.ModelAdmin):
    list_display=('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

