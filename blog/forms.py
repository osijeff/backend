from .models import Comment, Post
from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        


# create user form
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
class PostCreate(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'