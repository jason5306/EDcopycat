import profile
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms

from theBlog.models import Profile

class ProfileImgForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_img',)

class ProfilePageForm(forms.ModelForm):
    profile_img = forms.ImageField(required=False) 
    class Meta:
        model = Profile
        fields = ('bio', 'profile_img', 'link1', 'link1_name', 'link2', 'link2_name', 'link3', 'link3_name', 'link4', 'link4_name', 'link4', 'link5_name', 'link6', 'link6_name')

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            "link1" : forms.TextInput(attrs={'class': 'form-control'}),
            "link1_name" : forms.TextInput(attrs={'class': 'form-control'}),
            "link2" : forms.TextInput(attrs={'class': 'form-control'}),
            "link2_name" : forms.TextInput(attrs={'class': 'form-control'}),
            "link3" : forms.TextInput(attrs={'class': 'form-control'}),
            "link3_name" : forms.TextInput(attrs={'class': 'form-control'}),
            "link4" : forms.TextInput(attrs={'class': 'form-control'}),
            "link4_name" : forms.TextInput(attrs={'class': 'form-control'}),
            "link5" : forms.TextInput(attrs={'class': 'form-control'}),
            "link5_name" : forms.TextInput(attrs={'class': 'form-control'}),
            "link6" : forms.TextInput(attrs={'class': 'form-control'}),
            "link6_name" : forms.TextInput(attrs={'class': 'form-control'}),
            
        }

# inherit from UserCreationForm
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        #for visible in self.visible_fields():
        #    visible.field.widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        #self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'Username','style': 'font-size:24px;text-align: center;'})

        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

# inherit from UserChangeForm
class EditProfileForm(UserChangeForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    #last_login = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    #is_superuser = forms.CharField(required=True, max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    #is_staff = forms.CharField(required=True, max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    #is_active = forms.CharField(required=True, max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    #date_joined = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        # order of fields is the same as items will appear on screen
        #fields = ('username', 'first_name', 'last_name', 'email', 'password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined')
        fields = ('username', 'first_name', 'last_name', 'email')

# # inherit from PasswordChangeForm
class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
    new_password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
    new_password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')