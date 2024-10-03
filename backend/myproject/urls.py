"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from post.views import CategoryDetailView, CategoryListView, TagDetailView, TagListView
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version="v1",
        description="API Documentation for a Blog API",
        terms_of_service="https://github.com/okeneo/PersonalNest/blob/main/LICENSE",
        contact=openapi.Contact("okenetega@gmail.com"),
        license=openapi.License("MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/users/", include("account.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("api/posts/", include("post.urls")),
    path("api/categories/", CategoryListView.as_view(), name="category_list"),
    path("api/categories/<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
    path("api/tags/", TagListView.as_view(), name="tag_list"),
    path("api/tags/<int:pk>/", TagDetailView.as_view(), name="tag_detail"),
    re_path(
        r"^api/swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path("api/swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
