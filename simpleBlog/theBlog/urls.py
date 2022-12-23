import imp
from django.urls import path
#from django.conf.urls import url
#from . import views
from .views import AddPostView, DeletePostView, EditPostView, HomeView, ArticleDetailView, LikeView, AddCommentView, PostListView, reply_page, CommentDetailView, EditCommentView, DeleteCommentView, IndexPageView, SolveView, EndorseCommenttView, EndorsePostView, CommentNoticeListView,CommentNoticeUpdateView, SettingsPageView,ArchiveView,ArchiveCommenttView,ArchivePostView, Search,CourseListView#, AddCategortyView, CategoryView, CategoryListView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #path('', views.home, name = "home"),
    path('course/', login_required(CourseListView.as_view()), name = "course"),
    path('course/<int:course_id>/home/', login_required(HomeView.as_view()), name = "home"),
    path('course/<int:course_id>/home/<int:pk>', login_required(HomeView.as_view()), name = "home_frame"),
    path('archive/', ArchiveView.as_view(), name = "archive"),
    path('post_list/<int:course_id>/<str:filter>/<str:cat>', login_required(PostListView), name = "post_list"),
    # "pk" is the primary key of each blog
    path('article/<str:pk>', ArticleDetailView, name="article_detail"),
    path('article_archived/<str:pk>', ArticleDetailView, name="article_detail_archived"),
    path('course/<int:course_id>/new_post/', login_required(AddPostView.as_view()), name = 'new_post'),
    path('article/<int:pk>/edit', login_required(EditPostView.as_view()), name = 'edit_post'),
    path('article/<int:pk>/delete', login_required(DeletePostView.as_view()), name='delete_post'),
    # path('new_category/', login_required(AddCategortyView.as_view()), name = 'new_category'),
    # path('category/<str:cats>/', CategoryView, name='category'),
    # path('category_list/<str:user>/', CategoryListView, name='category_list'),
    path('like/<int:pk>', LikeView, name='like_post'),
    path('solved/<int:pk>/<int:id>/<int:cid>', SolveView, name='solved_view'),
    path('new_reply/', login_required(AddCommentView.as_view()), name = 'new_reply'),
    path('comment/reply/', reply_page, name="reply"),
    path('comment_detail/<int:pk>', login_required(CommentDetailView.as_view()), name="comment_detail"),
    path('comment/<int:pk>/edit', login_required(EditCommentView.as_view()), name = 'edit_comment'),
    path('comment/<int:pk>/delete', login_required(DeleteCommentView.as_view()), name='delete_comment'),
    path('index/', IndexPageView, name='index_page'),
    path('endorse_post/<int:pk>', login_required(EndorsePostView), name='endorse_post'),
    path('endorse_comment/<int:id>/<int:cid>', login_required(EndorseCommenttView), name='endorse_comment'),
    path('notice_list/<str:filter>', login_required(CommentNoticeListView), name="notice_list"),
    path('update_notice_list/', login_required(CommentNoticeUpdateView.as_view()), name="update_notice_list"),
    path('settings/', login_required(SettingsPageView), name='settings'),
    path('archived_post/<int:pk>', login_required(ArchivePostView), name='archived_post'),
    path('archived_comment/<int:id>/<int:cid>', login_required(ArchiveCommenttView), name='archived_comment'),
    path('course/<int:course_id>/search_result/', login_required(Search), name='search'),
] 