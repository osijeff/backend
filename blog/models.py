

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.

class Category(models.Model):
    
    name = models.CharField(max_length=250)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
      
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse()


class Post(models.Model):
    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blog_posts')
    post_image = models.ImageField(blank=True, null=True)
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES, default='draft')
    tags = TaggableManager()
    
    
    class Meta:
        ordering = ('-publish',)
        
        
    def __str__(self):
        return self.title
    
    
    def get_absolute_url(self):
        return reverse('post_detail', args=[self.publish.year,self.publish.month,self.publish.day, self.slug])
    

    
    
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    
    
    class Meta:
        ordering = ('created',)
    
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
