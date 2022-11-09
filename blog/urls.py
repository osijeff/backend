from django.urls import path
from . import views




urlpatterns = [
 # post views
 path('', views.post_list, name='post_list'),

 path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
 path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
 path('login/', views.loginView, name='login'),
 path('profile/', views.profileView, name='profile'),
 path('logout/', views.logout_view, name='logout'),
 path('add_post/', views.AddPostView.as_view(), name='add_post'),
 path('update_post/<int:pk>/', views.EditPostView.as_view(), name='update_post'),
 path('post_list/', views.PostListView.as_view(), name='post_list'),
 
#  delete
path('<id>/delete',  views.deletePost, name="delete_post"),
 
 
]