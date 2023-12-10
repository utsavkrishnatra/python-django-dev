from django.urls import path
from .views import UserSearch,RemoveFollower,AddFollower,PostListView,PostDetailView,PostEditView,PostDeleteView,CommentDeleteView,CommentEditView,ProfileView,ProfileEditView  # Import the PostListView class from views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post_list'),  # Use as_view() for class-based views
    # Add more paths as needed
    path('post/<int:pk>/',PostDetailView.as_view(),name='post_detail'),
    path('post/edit/<int:pk>/',PostEditView.as_view(),name='post_edit'),
    path('post/delete/<int:pk>/',PostDeleteView.as_view(),name='post_delete'),
    # path('comment/edit/<int:pk>/',CommentEditView.as_view(),name='comment_edit'),
    path('post/delete/<int:post_pk>/comment/<int:pk>/',CommentDeleteView.as_view(),name='comment_delete'),
    path('post/edit/<int:post_pk>/comment/<int:pk>/',CommentEditView.as_view(),name='comment_edit'),
    path('profile/<int:pk>/',ProfileView.as_view(),name='profile'),
    path('profile/edit/<int:pk>/',ProfileEditView.as_view(),name='edit_profile'),
    path('profile/<int:pk>/followers/add',AddFollower.as_view(),name='add_follower'),
    path('profile/<int:pk>/followers/remove',RemoveFollower.as_view(),name='remove_follower'),
    path('search/',UserSearch.as_view(),name='profile_search'),
    
]
