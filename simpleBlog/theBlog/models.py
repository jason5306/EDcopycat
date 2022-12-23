
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from datetime import datetime, date

from mdeditor.fields import MDTextField
from ckeditor.fields import RichTextField
# Create your models here.


class Profile(models.Model):
    # associated Profile with the User model
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_img = models.ImageField(blank=True, null=True, upload_to="images/profile_img")
    # for user social media links
    link1 = models.CharField(max_length=255, blank=True, null=True) 
    link2 = models.CharField(max_length=255, blank=True, null=True) 
    link3 = models.CharField(max_length=255, blank=True, null=True) 
    link4 = models.CharField(max_length=255, blank=True, null=True) 
    link5 = models.CharField(max_length=255, blank=True, null=True) 
    link6 = models.CharField(max_length=255, blank=True, null=True)
    link1_name = models.CharField(max_length=20, blank=True, null=True) 
    link2_name = models.CharField(max_length=20, blank=True, null=True) 
    link3_name = models.CharField(max_length=20, blank=True, null=True) 
    link4_name = models.CharField(max_length=20, blank=True, null=True) 
    link5_name = models.CharField(max_length=20, blank=True, null=True) 
    link6_name = models.CharField(max_length=20, blank=True, null=True)     
    


    def __str__(self):
        return str(self.user)
    def get_absolute_url(self):
        # set success url
        return reverse("show_profile", kwargs={'pk': self.pk})


class Category(models.Model):
    name = models.CharField(max_length=255, default = 'Uncategorized')
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        #return reverse("article_detail", args=(str(self.pk)))
        return reverse('home')
        #return reverse("article_detail", kwargs={'pk': self.pk})

class Course(models.Model):
    name = models.CharField(max_length=255)
    category = models.ManyToManyField(Category,related_name='course_cat')
    students = models.ManyToManyField(User, related_name = 'course_list')
    staff = models.ManyToManyField(User, related_name = 'course_staff')
    ta = models.ManyToManyField(User, related_name = 'course_ta')
    def __str__(self):
        return self.name
    def get_students(self):
        return self.students


class Post(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE, related_name="posts",null=True)
    title = models.CharField(max_length=255)
    # delete all blog post when delete the user
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    #body = models.TextField(default = 'default body')
    # header_image = models.ImageField(blank=True, null=True, upload_to="images/")
    # snippet = models.CharField(max_length=255, blank=True)
    body = MDTextField(blank=True, null=True) # for markdown content
    post_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=255, default = 'General')
    likes = models.ManyToManyField(User, related_name = 'blog_post')
    total_views = models.PositiveIntegerField(default=0)
    unique_views = models.ManyToManyField(User, related_name = 'unique_views')
    read = models.ManyToManyField(User, related_name = 'read', default=False)
    is_pin = models.BooleanField(default=False)
    solved_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_solved_by_user",null=True, blank=True ) 
    solved_by_comment = models.PositiveIntegerField(default=0)  
    endorsed = models.BooleanField(default=False)
    has_endorsed_comment = models.BooleanField(default=False)
    has_comment = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    has_archived_comment = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    private_viwers = models.ManyToManyField(User, related_name = 'private_viwers')

    def __str__(self):
        return self.title + ' | ' + str(self.author)
    
    def get_absolute_url(self):
        #return reverse("article_detail", args=(str(self.pk)))
        #return reverse('home')
        return reverse("article_detail", kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.count()
    
    def unique_views_count(self):
        return self.unique_views.count()

    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)
    def get_all_comments(self):
        return self.comments.filter(post=self.pk).filter(active=True)

# class Comment(models.Model):
#     post = models.ForeignKey(Post, related_name = "comments", on_delete=models.CASCADE) # referenced as 'comments' on blog pages
#     name = models.CharField(max_length=255)
#     body = models.TextField()
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return '%s - %s' % (self.post.title, self.name)
    
#     # def get_absolute_url(self):
#     # #return reverse("article_detail", args=(str(self.pk)))
#     # #return reverse('home')
#     #     return reverse("article_detail", kwargs={'pk': self.pk})

# comment model    
class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")
    # name=models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author",null=True, blank=True ) 
    parent=models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    #body = models.TextField()
    body = MDTextField(blank=False, null=True, config_name='custom') # for markdown content
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    endorsed = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return self.body
    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)
    def get_absolute_url(self):
        #return reverse("article_detail", args=(str(self.pk)))
        #return reverse('home')
        return reverse("article_detail", kwargs={'pk': self.post.pk})
