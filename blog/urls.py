from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('post/<int:pk>/', views.blog_post, name='blog-post'),
    path('post/<int:pk>/author', views.post_author, name='blog-post-author'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.blog_draft, name='blog-draft'),
    path('post/<int:pk>/publish/',views.publish_post, name='publish_post'),
    path('post/<pk>/delete', views.delete_post, name='delete_post'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
]