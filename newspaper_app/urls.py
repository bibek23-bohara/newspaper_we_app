from newspaper_app import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
   path(
    "", 
   views.HomeView.as_view(),
    name="home",
    ),
    path(

        "post-detail/<int:pk>/",
        views.PostDetailView.as_view(),
        name="post-detail",
    ),
    path(
    "post-list",
    views.PostListView.as_view(),
    name="post-list"
    ),
    path(
    "post-by-category/<int:cat_id>/",
    views.PostByCategoryView.as_view(),
    name="post-by-category"
    ),
     path(
    "post-by-tag/<int:cat_id>/",
    views.PostByTagView.as_view(),
    name="post-by-tag"
    ),
    path(
    "about/",
    views.AboutView.as_view(),
    name="about",
    ),
    path(
    "post-search/",
    views.PostSearchView.as_view(),
    name="post-search",
    ),
    path(
    "conatct/",
    views.Contactview.as_view(),
    name="contact",
    ),
    path(
    "newsletter/",
    views.NewsletterView.as_view(),
    name="newsletter",
    ),
    path(
    "comment//",
    views.CommentView.as_view(),
    name="comment",
    ),
    
]
