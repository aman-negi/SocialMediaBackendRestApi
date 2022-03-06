from django.urls import path
from .views import LoginView,LikePostView,UnlikePostView,GetAllPost,GetPost,Comment,FollowUserView,UnfollowUserView,ProfileView,DeletePost,CreatePostView


urlpatterns = [
    path('api/authenticate',LoginView.as_view()),
    path('api/follow/<str:pk>',FollowUserView.as_view()),
    path('api/unfollow/<str:pk>',UnfollowUserView.as_view()),
    path('api/user',ProfileView.as_view()),
    path('api/posts',CreatePostView.as_view()),
    path('api/posts/<str:pk>',CreatePostView.as_view()),
    path('api/like/<str:pk>',LikePostView.as_view()),
    path('api/unlike/<str:pk>',UnlikePostView.as_view()),
    path('api/comment/<str:pk>',Comment.as_view()),
    path('api/posts/<str:pk>',GetPost.as_view()),
    path('api/all_posts',GetAllPost.as_view()),
    path('api/delete',DeletePost.as_view()),   
]