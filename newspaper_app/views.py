from datetime import timedelta

from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import DetailView, ListView, TemplateView, View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, UpdateView, View)
from newspaper_app.forms import CommentForm, ContactForm, NewsletterForm, PostForm
from newspaper_app.models import Category, Post


class HomeView(ListView):
    model = Post
    template_name ="aznews/home.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(status="active", published_at__isnull=False).order_by("-published_at")[:5]


    def get_context_data(self, * args, **kwargs):
        context = super().get_context_data(* args, **kwargs)
        context["featured_post"]=(
            Post.objects.filter(status="active", published_at__isnull=False).order_by("-views_count").first()
        )
        context["featured_posts"]= Post.objects.filter(status="active", 
        published_at__isnull=False).order_by("-views_count")[2:5]
        one_week_ago = timezone.now() - timedelta(days=7)
        context["weekly_top_posts"]=Post.objects.filter(status="active", published_at__isnull=False,published_at__gte= one_week_ago,
        ).order_by("-published_at")[:7]
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = "aznews/detail.html"
    context_object_name ="post"

    def get_context_data(self, * args, **kwargs):
        context = super().get_context_data(* args, **kwargs)
        obj = self.get_object()
        context["previous_post"]=(
            Post.objects.filter(status="active", published_at__isnull=False, id__lt=obj.id).
            order_by("-id")
            .first()
        )
        context["next_post"]=(
            Post.objects.filter(status="active", published_at__isnull=False, id__gt=obj.id).
            order_by("id")
            .first()
        )
        context["recent_posts"]=(
            Post.objects.filter(status="active", published_at__isnull=False).order_by("-views_count")[:5]
        )
        return context

class PostListView(ListView):
    model = Post
    template_name = "aznews/main/list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(status="active", published_at__isnull=False).order_by("-published_at")
    paginate_by = 1

    
class PostByCategoryView(ListView):
    model = Post
    template_name = "aznews/main/list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(status="active", published_at__isnull=False).order_by("-published_at")
    paginate_by = 1

    def get_queryset(self):
        super().get_queryset()
        queryset = Post.objects.filter(
            status="active",
            published_at__isnull = False,
            category=self.kwargs["cat_id"],
        ).order_by("-published_at")
        return queryset
    

class PostByTagView(ListView):
    model = Post
    template_name = "aznews/main/list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(status="active", published_at__isnull=False).order_by("-published_at")
    paginate_by = 1

    def get_queryset(self):
        super().get_queryset()
        queryset = Post.objects.filter(
            status="active",
            published_at__isnull = False,
            category=self.kwargs["tags_id"],
        ).order_by("-published_at")
        return queryset

class AboutView(TemplateView):
    template_name = "aznews/main/about.html"


    def get_context_data(self, * args, **kwargs):
        context = super().get_context_data(* args, **kwargs)
        context["posts"]=(
            Post.objects.filter(status="active", published_at__isnull=False).
            order_by("-published_at")[:5]
        )
        return context
    
class PostSearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("query")
        post_list = Post.objects.filter(
            (Q(status ="active")& Q(published_at__isnull=False))&
            (Q(title__icontains=query) | Q(content__icontains=query)),
        )

        # paginator in function based views
        page = request.GET.get("page", 1)
        paginator = Paginator(post_list, 1)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)


        return render(
            request,
            "aznews/main/search_list.html",
            {"page_obj": posts, "query":query},
        )
    
class Contactview(View):
    template_name ="aznews/contact.html"
    form_class = ContactForm

    
    def get(self, request,*args,**kwargs):
        return render(request, self.template_name)
    

    def post(self, request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "successfully submitted your query. we will contact you soon."
            )
        else:
            messages.error(request, "cannot submit your query. something went wrong.")
        return render(
            request,
            self.template_name,
            {"form":form},
        )
 
class NewsletterView(View):
    form_class = NewsletterForm
    def post(self, request,*args,**kwargs):
        is_ajax = request.headers.get("x-requested-with")
        if is_ajax == "XMLHttpRequest":
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({
                    "success":True,
                    "message":"successfully submitted to our newsletter,",
                },
                status = 200,
                )
            else:
                return JsonResponse({
                    "success":False,
                    "message":"something went wrong."
                },
                status = 400,
                )
        else:
            return JsonResponse({
                "success":False,
                "message":"cannot processs. Must be an ajax request."
            },
            status = 400,
            )
        
class CommentView(View):
    form_class = CommentForm
    template_name = "aznews/detail.html"

    def post(self, request, *args, **kwargs):
        form =self.form_class(request.POST)
        post = request.POST["post"]
        if form.is_valid():
            form.save()
            return redirect("post-detail", post)
        else:
            post = Post.objects.get(pk=post)
            return render(
                request,
                self.template_name,
                {"post":post,"form":form},
            )
        





# def post_list(request):
#     posts = Post.objects.filter(
#         published_at__isnull=False).order_by("-published_at")
#     return render(
#         request,
#         "post_list.html",
#         {"posts": posts},


class DraftListView(ListView):
    model=Post
    template_name = "news_admin/post_list.html"
    context_object_name ="posts"
    queryset = Post.objects.filter(
        published_at__isnull=True).order_by("-published_at")

# @login_required
# def draft_list(request):
#     # ORM => Objects Relationship Mapping => convets to sQL
#     posts = Post.objects.filter(
#         published_at__isnull=True).order_by("-published_at")
#     return render(
#         request,
#         "post_list.html",
#         {"posts": posts},

#     ) 


# def post_detail(request, pk):
#     #post = Post.objects.get(pk=pk)
#     post = get_object_or_404(Post, pk=pk)
#     return render(
#         request,
#         "post_detail.html",
#         {"post": post},
#     )

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model =Post
    success_url = reverse_lazy("post-list")

    def form_valid(self,form):
        messages.success(self.request, "post was successfully deleted")
        return super().form_valid(form)
# @login_required
# def post_delete(request, pk):
#     #post = Post.objects.get(pk=pk)
#     post = get_object_or_404(Post, pk=pk)
#     post.delete()
#     messages.success(request,"post was successfully delete")
#     return redirect("post-list")




class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name ="news_admin/post_create.html"
    success_url = reverse_lazy("draft-list")

    def form_valid(self,form):
        form.instance.author = self.request.user
        messages.success(self.request, "post was successfully created")
        return super().form_valid(form)




def post_create(request):
    print('9999999III')
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request,"post was successfully created")
            return redirect("post-list")
        else:
            messages.error(request,"post was not created")
    return render(
        request,
        "post_create.html",
        {"form": form},
    )

class PostPublishView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk = pk)
        post.published_at = timezone.now()
        post.save()
        messages.success(request,"post was successfully published")
        return redirect("post-list")
        

# @login_required
# def post_publish(request, pk):
#     # post =Post.objects.get(pk=pk)
#     post = get_object_or_404(Post, pk=pk)
#     post.published_at = timezone.now()
#     post.save()
#     messages.success(request,"post was successfully published")
#     return redirect("post-list")




class PostUpdateView(LoginRequiredMixin, UpdateView):
    model= Post
    form_class =PostForm
    template_name ="news_admin/post_create.html"

# @login_required
# def post_update(request,pk):
#     post = Post.objects.get(pk=pk)
#     form = PostForm(instance=post)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"post was successfully updated")
#             return redirect("post-list")
#         else:
#             messages.success(request,"post was not updated ")
#     return render(
#         request,
#         "post_create.html",
#         {"form": form},
#     )



def handler404(request,exception, template_name="404.html"):
    return render(request, template_name, status=404)


