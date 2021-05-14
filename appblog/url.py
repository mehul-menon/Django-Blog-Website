from django.urls import path
from .views import PostListView,PostDetailView,PostListView,PostCreateView,PostUpdateView,PostDeleteView,UserPostListView,LikeView,AddCommentView
from . import views
# . refers to home directory
# we add variables to url to toggle between posts. pk means primary key
urlpatterns = [ 

    path('', PostListView.as_view(),name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(),name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(),name='post-detail'),
    path('post/new/', PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(),name='post-delete'),path('about/', views.about_page,name='About'),
    path('like/<int:pk>/', LikeView,name='like_post'),path('post/<int:pk>/comment/', AddCommentView.as_view(),name='add_comment')
]