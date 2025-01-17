from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('category/<int:pk>/', category_view, name="category"),
    path('article/<int:pk>/', article_detail, name="detail"),

    path('create_article/', create_article, name="create_article"),
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout', logout_view, name="logout"),
    path('article/<int:pk>/update/', ArticleUpdate.as_view(), name="update"),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name="delete"),
    path('comment/<int:article_id>/save/', save_comment, name='save_comment'),
    path('comment_delete/<int:comment_id>/', delete_comment, name='comment_delete'),
    path('comment/edit/<int:comment_id>/', edit_comment, name='edit_comment'),
    path('profile/<int:pk>/', profile_view, name='profile'),
    path('edit_profile/<int:pk>/', EditProfile.as_view(), name='edit'),
    path('edit_user/<int:pk>/', EditUser.as_view(), name='edit_user'),
    path('search/', SearchView.as_view(), name='search')
]
