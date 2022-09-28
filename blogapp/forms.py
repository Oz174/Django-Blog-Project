from wsgiref.validate import validator
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserSignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username','email','password1','password2']

class PostsForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        label = 'Post Title',
        widget= forms.TextInput(attrs={"placeholder": "Title..."})
    )
    content = forms.CharField(
        required = True , 
        label='',
        widget=forms.Textarea(attrs={"placeholder": "What are you thinking ...","rows":15,"cols":50}),
        validators=[validate_is_profane]
    )
    Tag = forms.CharField(
        required=False,
        label = 'Tag:',
    )
    post_pic = forms.ImageField(
        required= True,
        label = 'Upload the post picture: ',
        allow_empty_file=False,
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        empty_label='Choose Category'
    )
    
    class Meta: 
        model = Post
        fields = ['title', 'content','Tag' , 'category' ,'post_pic']

        def clean(self):
            cleaned_data = self.cleaned_data
            return cleaned_data

class CommentForm(forms.ModelForm):
    bodytext = forms.CharField(
        required = True , 
        label='',
        widget=forms.Textarea(attrs={"placeholder":"Your comment ...","rows":3,"cols":50}),
        validators=[validate_is_profane]
    )
    class Meta: 
        model  = Comment
        fields = ['bodytext']
    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data