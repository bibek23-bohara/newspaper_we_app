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
    path("post-delete/<int:pk>/",
        views.PostDeleteView.as_view(),
        name="post-delete"),
    
    path("post-update/<int:pk>/",
    views.PostUpdateView.as_view(),
    name="post-update"),
    path(
    "post-create/",
    views.PostCreateView.as_view(),
    name="post-create"
    ),
    path(
        "draft-list/",
        views.DraftListView.as_view(),
        name="draft-list",
    ),
    path("post-publish/<int:pk>/",
            views.PostPublishView.as_view(),
            name="post-publish",
            ),

    path(
    "draft-detail/",
        views.DraftDetailView.as_view(),
        name="draft-detail",
        ),

    path("tag-list/",
        views.TagListView.as_view(),
        name="tag-list",
        ), 
    path("tag-create/",
        views.TagCreateView.as_view(),
        name="tag-create",
        ), 
        path("tag-update/",
        views.TagUpdateView.as_view(),
        name="tag-update",
        ), 
        path("tag-delete/",
        views.TagDeleteView.as_view(),
        name="tag-delete",
        ), 
         path("category-list/",
        views.CategoryListView.as_view(),
        name="category-list",
        ), 
    path("category-create/",
        views.CategoryCreateView.as_view(),
        name="category-create",
        ), 
        path("category-update/",
        views.CategoryUpdateView.as_view(),
        name="category-update",
        ), 
         path("category-delete/",
        views.CategoryDeleteView.as_view(),
        name="category-delete",
        ), 



         
    
    
]
