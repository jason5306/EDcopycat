from symbol import file_input
from tkinter.tix import IMMEDIATE
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect

from theBlog.models import Profile

from .forms import RegisterForm, EditProfileForm, PasswordChangingForm, ProfilePageForm, ProfileImgForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import DetailView, UpdateView, CreateView

def ChangeProfileImgView(request, id):
    profile_img_form = ProfileImgForm(request.POST, request.FILES)
    current_profile = get_object_or_404(Profile, id=id)
    if profile_img_form.is_valid():
        if 'profile_img' in request.FILES:
            current_profile.profile_img = request.FILES['profile_img']
            current_profile.save()


    # return render(request, 'registration/profile_img.html',{'current_profile':current_profile})
    # return reverse_lazy('show_profile')
    return HttpResponseRedirect(reverse('show_profile', kwargs={'pk': id}))
   



class CreateProfilePageView(CreateView):
    model = Profile
    template_name = 'registration/create_profile_page.html'
    #fields ='__all__'
    form_class = ProfilePageForm

    def form_valid(self, form):
        form.instance.user = self.request.user # get the current user who's filling out the form
        return super().form_valid(form)

class EditProfilePageView(UpdateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = 'registration/edit_profile_page.html'


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'
    
    
    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfilePageView, self).get_context_data(
            *args, **kwargs)
        current_user = get_object_or_404(
            Profile, id=self.kwargs['pk'])  # lookup the owner of the profile

        context['current_user'] = current_user
        return context

class UserRegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class UserSettingView(UpdateView):
    form_class = EditProfileForm # UserChangeForm 
    template_name = 'registration/edit_settings.html'
    success_url = reverse_lazy('course')    

    def get_object(self):
        return self.request.request

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm

    def get_success_url(self):
        return reverse_lazy("show_profile", kwargs={'pk': self.request.user.profile.id})

