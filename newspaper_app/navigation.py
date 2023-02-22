from django.db.models import F, Sum, Case, When
from newspaper_app.models import Category, Post, Tag

def navigation(request):
    catgegories = Category.objects.all()
    tags = Tag.objects.all()[:10]
    top_categories = (
        Post.objects.values("category__pk","category__name")
        .annotate(
            pk=F("category__pk"), name=F("category__name"), max_views=Sum("views_count")
            )
            .order_by("-views_count") # order in discending order
            .values("pk","name","max_views")# fatch only pk and name 
    )
    # whats_new_categories = Category.objects.filter(
    #          pk__in = [top_categories["pk"] for top_categories in top_categories]
    #         # pk__in = [4,1,6]
    # )
    print(top_categories)
    category_ids = [top_category["pk"] for top_category in top_categories]
    order_by_max_view = Case(
        *[
         When(
        id= category["pk"], then=category["max_views"]
         )
        for category in top_categories
        ]
    )
    whats_new_categories = Category.objects.filter(pk__in=category_ids).order_by(
        -order_by_max_view
    )[:2]
    top_categories = Category.objects.filter(pk__in= category_ids).order_by(
        -order_by_max_view
    )[:2]

    print(top_categories)

    return{
        "categories":catgegories,
        "tags":tags,
        "top_categories":top_categories,
        "whats_new_categories":whats_new_categories
    }