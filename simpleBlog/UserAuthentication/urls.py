from django.urls import path
from .views import UserSettingView, UserRegisterView, PasswordsChangeView, ShowProfilePageView, EditProfilePageView, CreateProfilePageView,ChangeProfileImgView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name = 'register'),
    path('edit_settings/', login_required(UserSettingView.as_view()), name = 'edit_settings'),
    #path('password/', auth_views.PasswordChangeView.as_view(template_name="registration/change_password.html")),
    path('password/', login_required(PasswordsChangeView.as_view(template_name="registration/change_password.html")), name="password"),
    path('<int:pk>/profile/', ShowProfilePageView.as_view(), name = 'show_profile'),
    path('<int:pk>/edit_profile_page/', login_required(EditProfilePageView.as_view()), name = 'edit_profile_page'),
    path('create_profile_page/', login_required(CreateProfilePageView.as_view()), name = 'create_profile_page'),
    path('change_profile_img/<int:id>', login_required(ChangeProfileImgView), name = 'change_profile_img'),
] 