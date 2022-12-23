from dataclasses import fields
from django import forms
from .models import Post, Category, Comment, User, Course
from django.shortcuts import get_object_or_404

# query names from Category
choices = Category.objects.all().values_list('name', 'name')
choice_list = []
for item in choices: # retrieve from 'choices'
    choice_list.append(item)



class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """ Unpack kwargs from get_form_kwargs() at AddPostView"""
        current_course_id = kwargs.pop('course_id')        
        super(PostForm, self).__init__(*args, **kwargs)
        
        # init private viewers
        current_course = get_object_or_404(Course, id=current_course_id)
        private_viwers_list = []
        for staff in current_course.staff.all():
            private_viwers_list.append((staff.id, str(staff.first_name)+' '+str(staff.last_name) + ' | Staff'))
        for ta in current_course.ta.all():
            private_viwers_list.append((ta.id, str(ta.first_name)+' '+str(ta.last_name) + ' | TA'))              
        self.fields['private_viwers'].choices = private_viwers_list

        # init category list
        category_list_choices = current_course.category.all().values_list('name', 'name')
        category_list = []
        for cat in category_list_choices: # retrieve from 'choices'
            category_list.append(cat)
        self.fields['category'].widget.choices = category_list
        
    private_viwers = forms.MultipleChoiceField(choices=[],widget=forms.SelectMultiple(attrs={'class': 'form-select','size':'3'}),required=False)
    category = forms.CharField(widget=forms.Select(choices=[], attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ('title', 'author', 'category','body', 'is_pin', 'course','is_private','private_viwers')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input your post title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'author_id', 'type':'hidden'}),
            #'author': forms.Select(attrs={'class': 'form-control'}),
            # 'category': forms.Select(choices=[], attrs={'class': 'form-control'}),
            # 'snippet': forms.Textarea(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'is_pin': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'course': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'course_id', 'type':'hidden'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            #'private_viwers': forms.SelectMultiple(choices=tuple(private_viwers_list)),
        }

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category','is_pin','body')
        labels = {
            "is_pin":  "Pin the post?",
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            #'author': forms.Select(attrs={'class': 'form-control'}),
            # 'snippet': forms.Textarea(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'is_pin': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
        }

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('name', 'body')

#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'body': forms.Textarea(attrs={'class': 'form-control'}),
            
#         }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('post','author','parent', 'body')
        widgets = {
            'post': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'id_post', 'type':'hidden'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'author_id', 'type':'hidden'}),
            'parent': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'id_parent', 'type':'hidden'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            
        }
    
    # overriding default form setting and adding bootstrap class
    # def __init__(self, *args, **kwargs):
    #     super(CommentForm, self).__init__(*args, **kwargs)
    #     self.fields['name'].widget.attrs = {'placeholder': 'Enter name','class':'form-control', 'type':'hidden'}
    #     self.fields['email'].widget.attrs = {'placeholder': 'Enter email', 'class':'form-control'}
    #     self.fields['body'].widget.attrs = {'placeholder': 'Comment here...', 'class':'form-control', 'rows':'5'}