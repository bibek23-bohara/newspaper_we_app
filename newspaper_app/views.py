from datetime import timedelta
from django.http import JsonResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, TemplateView, View
from newspaper_app.models import Post, Category 
from newspaper_app.forms import ContactForm,NewsletterForm, CommentForm
from django.contrib import messages
from django.db.models import Q
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


