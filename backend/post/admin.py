from django.contrib import admin

from .models import Category, Post, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post

    list_filter = (
        "published",
        "publish_date",
    )


# list_editable = (
#     "title",
#     "subtitle",
#     "slug",
#     "publish_date",
#     "published",
# )
# search_fields = (
#     "title",
#     "subtitle",
#     "slug",
#     "body",
# )
# prepopulated_fields = {
#     "slug": (
#         "title",
#         "subtitle",
#     )
# }
