from django.shortcuts import render, get_object_or_404, redirect
from .models import Post,  Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm, CreateUserForm, PostCreate
from taggit.models import Tag
from django.db.models import Count
from django.contrib.auth.decorators import login_required


from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from django.contrib.auth import login, authenticate #add this

# from django.views.generic.edit import CreateView
from django.views.generic import (
    CreateView, 
    ListView, 
    UpdateView, 
    DetailView, 
    DeleteView
)
# from django.views import generic
from django.urls import reverse_lazy
# Create your views here.

#  view for all posts
def post_list(request, tag_slug=None):
    object_list = Post.objects.all()
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 8) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
 # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
 # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,'index.html', {"page":page,'posts': posts, 'tag': tag})

# view for single post
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
        # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    return render(request,'post_detail.html',{'post': post,'comments': comments,'new_comment': new_comment,'comment_form': comment_form, "similar_posts":similar_posts})


def loginView(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("profile")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()            
    return render(request, 'registration/login.html', context={"form":form})


@login_required(login_url='login')
def profileView(request):
    return render(request, 'profile.html', { })








def logout_view(request):
    logout(request)
    return redirect('/')
   
   


def upload(request):
    upload = PostCreate()
    if request.method == 'POST':
        upload = PostCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('post_list')
        
    else:
         return render(request, 'createpost.html', {'upload':upload})
            



# create a new post view
class AddPostView(CreateView):
    model= Post
    template_name='addBlogPost.html'
    fields = '__all__'
    
    success_url = reverse_lazy('profile')
    
    
class PostListView(ListView):
    model = Post
    template_name = "profile.html"

class EditPostView(UpdateView):
    model= Post
    template_name='editPost.html'
    fields = '__all__'
    
    success_url = reverse_lazy('profile')
    
    

# delete post
@login_required
def deletePost(request, id):
    post_del =get_object_or_404(Post, id = id)
    post_del.delete()
    messages.error(request, 'Post was deleted successfully!')
    return redirect('profile')
    
