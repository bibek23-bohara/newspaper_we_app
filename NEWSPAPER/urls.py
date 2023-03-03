
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    #third party urls
    path('summernote/', include('django_summernote.urls')),
    path("accounts/login/" , LoginView.as_view(), name="login"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    #custom urls
    path("",include("newspaper_app.urls",)),
    path("api/v1/", include("api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "newspaper_app.views.handler404"