from django.shortcuts import render, get_object_or_404,redirect, get_list_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views import View
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse


from .models import Category, Post, Comment, User,Course
from .forms import PostForm, EditPostForm, CommentForm
from .sendemail import *
import markdown
from markdown.extensions.toc import TocExtension
from notifications.signals import notify
import time
from datetime import datetime
from django.utils import timesince

from django.core.mail import send_mail
import re
from django.db import models


# Create your views here.
# def home(request):
#    return render(request, 'home.html', {})

# class CommentNoticeListView(ListView):
#     context_object_name = 'notices'
#     template_name = 'notice_list.html'
#     def get_queryset(self):
#         return self.request.user.notifications.active()


def Search(request, course_id):
    if request.method == 'POST':
        search = request.POST.get('search')

        query_post = Post.objects.filter(
            models.Q(course=course_id) &
            (models.Q(title__icontains=search) |
            models.Q(author__first_name__icontains=search) |
            models.Q(author__last_name__icontains=search) |
            models.Q(body__icontains=search) |
            models.Q(comments__body__icontains=search))
        ).distinct()

        query_post = query_post.filter(
            models.Q(is_private=False) |
            (models.Q(is_private=True) & models.Q(private_viwers=request.user)) |
            (models.Q(author=request.user))
        ).distinct()

        

    return render(request, 'search_result.html',{'search':search,'query_post':query_post})

class ArchiveView(ListView):
    model = Post
    template_name = 'archive_page.html'
    ordering = ['-edit_date']
    def get_context_data(self, *args, **kwargs):
        context = super(ArchiveView, self).get_context_data(*args, **kwargs)       
        post_list = Post.objects.filter(models.Q(archived=True) | models.Q(has_archived_comment=True)).order_by('-edit_date')

        context['post_list'] = post_list

        
        # context['object_list'] = object_list
        # context['post'] = current_post
        return context
    

def SettingsPageView(request):
    return render(request, 'settings_page.html')

def CommentNoticeListView(request, filter):
    notices = request.user.notifications.active()
    
    if 'unread' in filter:
        notices = request.user.notifications.unread()
    
    notice_dict = {}
    for notice in notices:
        notice_timestamp = timesince.timesince(notice.timestamp,depth=1)
        if 'hour' in notice_timestamp or 'minute' in notice_timestamp:
            if 'Today' in notice_dict:
                notice_dict['Today'].append(notice)
            else:
                notice_dict['Today'] = []
                notice_dict['Today'].append(notice)
        else:
            if notice_timestamp in notice_dict:
                notice_dict[notice_timestamp].append(notice)
            else:
                notice_dict[notice_timestamp] = []
                notice_dict[notice_timestamp].append(notice)


    return render(request, 'notice_list.html',{'notices':notices,'notice_dict':notice_dict})

class CommentNoticeUpdateView(View):
    def get(self, request):
        notice_id = request.GET.get('notice_id')
        if notice_id:
            post = Post.objects.get(id=request.GET.get('post_id'))
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(post)
        
        else:
            request.user.notifications.mark_all_as_read()
            
            return HttpResponseRedirect(reverse('notice_list', args=['all']))

def IndexPageView(request):
    return render(request, 'index_page.html')


# class PostListView(ListView):
#     model = Post
#     template_name = 'post_list.html'
#     ordering = ["-is_pin",'-edit_date']
def PostListView(request,course_id,filter,cat):

    object_list = Post.objects.filter(course=course_id)

    if filter == 'all' and cat == 'all':
        object_list = Post.objects.filter(course=course_id)

    else:
        if cat != 'all':
            object_list = Post.objects.filter(
                models.Q(course=course_id)&
                models.Q(category=cat))            
        if filter == 'unread':
            object_list = object_list.filter(
                models.Q(course=course_id)&
                models.Q(read=None))
        elif filter == 'unanswered':
            object_list = object_list.filter(
                models.Q(course=course_id)&
                models.Q(has_comment=False))
        elif filter == 'unresolved':
            object_list = object_list.filter(
                models.Q(course=course_id)&
                models.Q(solved_by_comment=0))
        elif filter == 'endorsed_post':
            object_list = object_list.filter(
                models.Q(course=course_id)&
                models.Q(endorsed=True))
        elif filter == 'endorsed_comment':
            object_list = object_list.filter(
                models.Q(course=course_id)&
                models.Q(has_endorsed_comment=True))
        elif filter == 'mine': 
            object_list = object_list.filter(
                models.Q(course=course_id)&
                models.Q(author_id = request.user.id))
        elif filter == 'private':
            object_list = object_list.filter(
                models.Q(course=course_id)&
                models.Q(is_private=True))

    # filter out accessible posts
    object_list = object_list.filter(
            models.Q(is_private=False) |
            (models.Q(is_private=True) & models.Q(private_viwers=request.user)) |
            (models.Q(author=request.user))
        ).distinct()
    
    
    post_dict = {}
    object_list_pin = object_list.filter(is_pin=True).order_by('-edit_date')
    object_list_others = object_list.filter(is_pin=False).order_by('-edit_date')
    post_dict['Pin'] = object_list_pin
    for post in object_list_others:
        post_timestamp = timesince.timesince(post.edit_date,depth=1)
        if 'hour' in post_timestamp or 'minute' in post_timestamp:
            if 'Today' in post_dict:
                post_dict['Today'].append(post)
            else:
                post_dict['Today'] = []
                post_dict['Today'].append(post)
        else:
            if post_timestamp in post_dict:
                post_dict[post_timestamp].append(post)
            else:
                post_dict[post_timestamp] = []
                post_dict[post_timestamp].append(post)
    if len(post_dict['Pin']) == 0:
        post_dict.pop("Pin", None)

    return render(request, 'post_list.html',{'post_dict':post_dict})



class CourseListView(ListView):
    model = Course
    template_name = 'course_list.html'
    def get_context_data(self, *args, **kwargs):
        context = super(CourseListView, self).get_context_data(*args, **kwargs)  
        current_user = get_object_or_404(User, id=self.request.user.id)    
        user_course_list = current_user.course_list.all()
        context['user_course_list'] = user_course_list
        

        return context

class HomeView(ListView):
    model = Post
    template_name = 'home.html'

    #ordering = ['-id']
    ordering = ["-is_pin",'-edit_date']
    # def get_context_data(self, *args, **kwargs):
    #    cat_menu = Category.objects.all()
    #    context = super(HomeView, self).get_context_data(*args, **kwargs)
    #    context["cat_menu"] = cat_menu
    #    return context

    def get_context_data(self, *args, **kwargs):

        
        context = super(HomeView, self).get_context_data(*args, **kwargs)       
        current_course_id = self.kwargs['course_id']
        current_course = get_object_or_404(Course, id=current_course_id)
        
        post_accessible = Post.objects.filter(
            models.Q(is_private=False) |
            (models.Q(is_private=True) & models.Q(private_viwers=self.request.user)) |
            (models.Q(author=self.request.user))
        ).distinct()

        post_all = post_accessible.filter(
            models.Q(course=current_course_id) &
            models.Q(is_pin=False)
            ).order_by('-edit_date')
        post_pin = post_accessible.filter(
            models.Q(course=current_course_id) &
            models.Q(is_pin=True)
            ).order_by('-edit_date')

        # group post by date
        post_dict = {}
        post_dict['Pin'] = post_pin
        for post in post_all:
            post_timestamp = timesince.timesince(post.edit_date,depth=1)
            if 'hour' in post_timestamp or 'minute' in post_timestamp:
                if 'Today' in post_dict:
                    post_dict['Today'].append(post)
                else:
                    post_dict['Today'] = []
                    post_dict['Today'].append(post)
            else:
                if post_timestamp in post_dict:
                    post_dict[post_timestamp].append(post)
                else:
                    post_dict[post_timestamp] = []
                    post_dict[post_timestamp].append(post)
        ## pop up key when no post is pinned            
        if len(post_dict['Pin']) == 0:
            post_dict.pop("Pin", None)                    

        cat_menu_list = get_object_or_404(Course, id=current_course_id).category.all()
        
        cat_post_count = []
        for cat in cat_menu_list:
            cat_post_count.append(
                [cat, len(Post.objects.filter(
                    models.Q(category=cat)&models.Q(course=current_course_id)
                    ))])
                
        # for post in Post.objects.all():
        #     print(post.get_all_comments())
        #     for comment in post.get_all_comments():

        #     print('---')

        # object_list = Post.objects.all()
        
        current_url = self.request.get_full_path().split("home/")[1]
        iframe_src = "index_page"
        if current_url != '':
            iframe_src = current_url
            
            
        
        
        context['cat_post_count'] = cat_post_count
        context['post_dict']= post_dict
        context['iframe_src']= iframe_src
        context['current_course_id'] = current_course_id
        context['current_course'] = current_course
        
        # context['object_list'] = object_list
        # context['post'] = current_post
        return context

def ArticleDetailView(request, pk):
    post=get_object_or_404(Post,id=pk)
    # mark current user as read this post
    # post.read = True
    # post.save(update_fields=['read'])
    
    if not post.read.filter(id=request.user.id).exists():
        if not request.user.id is None:
            post.read.add(request.user)
    # update total views
    post.total_views += 1
    post.save(update_fields=['total_views'])
    # update unique views
    if not post.unique_views.filter(id=request.user.id).exists():
        if not request.user.id is None:
            post.unique_views.add(request.user)

    unique_views_count = post.unique_views_count()
    
    # likes
    total_likes = post.total_likes()
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True

    new_comment = None
    comment_form = CommentForm()
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        comment_form.instance.name = request.user.id
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()

            # send notification
            if new_comment.parent is None:
                notify.send(
                    request.user,
                    recipient = post.author,
                    verb = 'commented',
                    target=post,
                    description='comment'
                )
                # send_mail(
                # 'Subject here',
                # 'Here is the link: http://' + request.get_host() + "/home/" + str(post.pk),
                # 'fromjiacheng@example.com',
                # [post.author.email],
                # fail_silently=False,
                # )
                email_subject = 'New comment under your post.'
                email_data = {
                    'who': str(request.user.first_name) + " " + str(request.user.last_name),
                    'action': 'commented',
                    'object': post,
                    'object_type': 'post',
                    'link': 'http://' + request.get_host() + "/home/" + str(post.pk),
                    'content': new_comment.body
                }
                email_template = "notification_email.html"
                to_list = [post.author.email,]
                send_email_by_template(email_subject,email_template,email_data,to_list)

            else:
                notify.send(
                    request.user,
                    recipient = post.author,
                    verb = 'replied',
                    target=post,
                    description='reply'
                )
                email_subject = 'New reply under your comment.'
                email_data = {
                    'who': str(request.user.first_name) + " " + str(request.user.last_name),
                    'action': 'replied',
                    'object': post,
                    'object_type': 'comment under post',
                    'link': 'http://' + request.get_host() + "/home/" + str(post.pk),
                    'content': new_comment.body
                }
                email_template = "notification_email.html"
                to_list = [post.author.email,]
                send_email_by_template(email_subject,email_template,email_data,to_list)

            # redirect to same page and focus on that comment
            # return redirect(post.get_absolute_url()+'#'+str(new_comment.id))
            return redirect(post.get_absolute_url())
        else:
            comment_form = CommentForm()
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    if len(comments) > 0:
        post.has_comment = True
    else:
        post.has_comment = False
    post.save()
    # granted viewers
    # in addition to block users from seeing the private post from the post list, this blocks users who try to access private posts via urls
    accessible = (not post.is_private) or (post.is_private and request.user in post.private_viwers.all()) or (post.is_private and request.user.id == post.author.id)
    

    return render(request, 'article_detail.html',{'post':post,'comments': comments,'comment_form':comment_form, 'total_likes':total_likes, 'liked':liked, 'unique_views_count':unique_views_count,'accessible':accessible})



# class ArticleDetailView(DetailView):
#     model = Post
#     template_name = 'article_detail.html'
    
    

#     def get_context_data(self, *args, **kwargs):
#         #cat_menu = Category.objects.all()
#         context = super(ArticleDetailView, self).get_context_data(
#             *args, **kwargs)

#         current_post = get_object_or_404(
#             Post, id=self.kwargs['pk'])  # lookup the blog with the pk
#         # like button
#         total_likes = current_post.total_likes()
#         liked = False
#         if current_post.likes.filter(id=self.request.user.id).exists():
#             liked = True
#         # comment
#         comments = current_post.comments.filter(active=True)
#         new_comment = None
#         comment_form = CommentForm(data=self.request.POST)
#         if self.request.method == 'POST':
#             comment_form = CommentForm(data=self.request.POST)
#             if comment_form.is_valid():
#                 # Create Comment object but don't save to database yet
#                 new_comment = comment_form.save(commit=False)
#                 # Assign the current post to the comment
#                 new_comment.post = current_post
#                 # Save the comment to the database
#                 new_comment.save()
#                 return redirect(current_post.get_absolute_url()+'#'+str(new_comment.id))
#             else:
#                 comment_form = CommentForm()

#         # context data
#         context['total_likes'] = total_likes
#         context['liked'] = liked
#         # context['post'] = current_post
#         return context

# deprecated
def reply_page(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id')  # from hidden input
            parent_id = request.POST.get('parent')  # from hidden input
            post_url = request.POST.get('post_url')  # from hidden input
            reply = form.save(commit=False)
    
            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()
            return redirect(post_url+'#'+str(reply.id))
    return redirect("/")


class AddPostView(CreateView):
    model = Post    
    form_class = PostForm
    template_name = 'new_post.html'
    # Can choose from POST eg.
    # fields = ('title', 'body')
    # fields = '__all__'
    def get_context_data(self, *args, **kwargs):
        context = super(AddPostView, self).get_context_data(*args, **kwargs)     
        context['course_id'] = self.kwargs['course_id']
        return context
    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to get current course attributes"""

        kwargs = super(AddPostView, self).get_form_kwargs()
        
        kwargs['course_id'] = self.kwargs['course_id']
        return kwargs
        

class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'new_reply.html'
    
    # success_url = reverse_lazy('home')
    def get_success_url(self):
        return reverse_lazy('home')

    
# deprecated
class CommentDetailView(DetailView):
    model = Comment
    template_name = 'comment_detail.html'

class EditCommentView(UpdateView):
    model = Comment
    template_name = 'edit_comment.html'
    form_class = CommentForm
    
    

class DeleteCommentView(DeleteView):
    model = Comment
    def get_success_url(self):
        current_comment = Comment.objects.get(id=self.kwargs["pk"])
        return reverse_lazy("article_detail", kwargs={'pk': current_comment.post.pk})

class EditPostView(UpdateView):
    model = Post
    template_name = 'edit_post.html'
    form_class = EditPostForm


class DeletePostView(DeleteView):
    model = Post
    success_url = reverse_lazy('index_page')

# depreciated
class AddCategortyView(CreateView):
    model = Category
    #form_class = PostForm
    template_name = 'new_category.html'
    # Can choose from POST eg.
    # fields = ('title', 'body')
    fields = '__all__'

# function based view


# def CategoryView(request, cats):
#     category_posts = Post.objects.filter(category=cats)  # get post under a cat
#     return render(request, 'category_page.html', {'cats': cats, 'category_posts': category_posts})


# def CategoryListView(request, user):
#     cat_menu_list = Category.objects.all()
#     cat_post_count = []
#     for cat in cat_menu_list:
#         cat_post_count.append(
#             [cat, len(Post.objects.filter(category=cat, author=user))])
#     return render(request, 'category_list_page.html', {'cat_post_count': cat_post_count})


def LikeView(request, pk):
    post = get_object_or_404(Post, id=pk)
    liked = True
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        total_likes = post.total_likes()
        liked = False
    else:
        liked = True
        post.likes.add(request.user)
        total_likes = post.total_likes()
        notify.send(
        request.user,
        recipient = post.author,
        verb = 'liked',
        target=post,
        description='like'
    )
    # return HttpResponseRedirect(reverse('article_detail', args=[str(pk)]))
    return render(request, 'like_view.html',{'liked':liked,'total_likes':total_likes})

def SolveView(request, pk, id, cid):
    post = get_object_or_404(Post, id=pk)
    # not resolved
    solved = True
    if post.solved_by_comment == 0: 
        post.solved_by_comment = cid # store comment id
        
        post.solved_by_user = get_object_or_404(User,id=id)
        post.save()
        solved = True
        notify.send(
        request.user,
        recipient = get_object_or_404(User,id=id),
        verb = 'solved',
        target=post,
        description='solution'
        )
        email_subject = 'Your comment is marked as solution.'
        email_data = {
            'who': str(request.user.first_name) + " " + str(request.user.last_name),
            'action': 'has marked',
            'object': post,
            'object_type': 'comment as solution to',
            'link': 'http://' + request.get_host() + "/home/" + str(post.pk),
            # 'content': ''
        }
        email_template = "notification_email.html"
        to_list = [post.author.email,]
        send_email_by_template(email_subject,email_template,email_data,to_list)
    # remove solution
    else:
        post.solved_by_comment = 0
        post.solved_by_user = None
        post.save()
        solved = False

    # return HttpResponseRedirect(reverse('article_detail', args=[str(post.pk)]))
    return render(request, 'post_resolve_view.html',{'solved':solved,'comment_id':cid})

def EndorsePostView(request, pk):
    post = get_object_or_404(Post, id=pk)
    endorsed = True
    if post.endorsed:
        post.endorsed = False
        post.save()
        endorsed = False
    else:
        post.endorsed = True
        post.save()
        endorsed = True
        notify.send(
        request.user,
        recipient = post.author,
        verb = 'endorsed',
        target=post,
        description='endorse'
        )
        email_subject = 'Your post is endorsed.'
        email_data = {
            'who': str(request.user.first_name) + " " + str(request.user.last_name),
            'action': 'endorsed',
            'object': post,
            'object_type': 'post',
            'link': 'http://' + request.get_host() + "/home/" + str(post.pk),
            # 'content': ''
        }
        email_template = "notification_email.html"
        to_list = [post.author.email,]
        send_email_by_template(email_subject,email_template,email_data,to_list)

    # return HttpResponseRedirect(reverse('article_detail', args=[str(pk)]))
    return render(request, 'endorse_view.html',{'endorsed':endorsed})

def EndorseCommenttView(request, id, cid):
    comment = get_object_or_404(Comment, id=cid)
    post = get_object_or_404(Post, id=id)
    endorsed = True
    if comment.endorsed:
        comment.endorsed = False
        comment.save()
        endorsed = False
    else:
        comment.endorsed = True
        comment.save()
        endorsed = True
        notify.send(
        request.user,
        recipient = comment.author,
        verb = 'endorsed',
        target=post,
        description='endorsec'
        )
        email_subject = 'Your comment is endorsed.'
        email_data = {
            'who': str(request.user.first_name) + " " + str(request.user.last_name),
            'action': 'endorsed',
            'object': post,
            'object_type': 'comment under post',
            'link': 'http://' + request.get_host() + "/home/" + str(post.pk),
            # 'content': ''
        }
        email_template = "notification_email.html"
        to_list = [post.author.email,]
        send_email_by_template(email_subject,email_template,email_data,to_list)        

    # allow multiple comment to be endorsed
    if post.comments.filter(endorsed=True).count() > 0:
        post.has_endorsed_comment = True
        post.save()
    else:
        post.has_endorsed_comment = False
        post.save()

    
    # return HttpResponseRedirect(reverse('article_detail', args=[str(id)]))
    return render(request, 'endorse_comment_view.html',{'endorsed':endorsed})

def ArchivePostView(request, pk):
    post = get_object_or_404(Post, id=pk)
    archived = True
    if post.archived:
        post.archived = False
        post.save()
        archived = False
    else:
        post.archived = True
        post.save()
        archived = True

    return render(request, 'archived_post_view.html',{'archived':archived})

def ArchiveCommenttView(request, id, cid):
    comment = get_object_or_404(Comment, id=cid)
    post = get_object_or_404(Post, id=id)
    archived = True
    if comment.archived:
        comment.archived = False
        comment.save()
        archived = False
    else:
        comment.archived = True
        comment.save()
        archived = True
    # allow multiple comment to be endorsed
    if post.comments.filter(archived=True).count() > 0:
        post.has_archived_comment = True
        post.save()
    else:
        post.has_archived_comment = False
        post.save()

    
    # return HttpResponseRedirect(reverse('article_detail', args=[str(id)]))
    return render(request, 'archived_comment_view.html',{'archived':archived})    