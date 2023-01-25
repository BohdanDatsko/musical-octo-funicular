from django.urls import path


from apps.api.views import (
    CommentListCreateApiView,
    CommentLikeUnlikeApiView,
    PostListCreateApiView,
    PostLikeUnlikeApiView,
    CommentDetailApiView,
    PostDetailApiView,
)

app_name = "api"

urlpatterns = [
    path("posts/", PostListCreateApiView.as_view(), name="api_posts_list_create"),
    path("posts/<int:post_pk>/", PostDetailApiView.as_view(), name="api_post_detail"),
    path(
        "posts/<int:post_pk>/like/",
        PostLikeUnlikeApiView.as_view({"post": "like"}),
        name="api_post_like",
    ),
    path(
        "posts/<int:post_pk>/unlike/",
        PostLikeUnlikeApiView.as_view({"post": "unlike"}),
        name="api_post_unlike",
    ),
    path(
        "posts/<int:post_pk>/fans/",
        PostLikeUnlikeApiView.as_view({"get": "fans"}),
        name="api_post_fans",
    ),
    path(
        "posts/<int:post_pk>/comments/",
        CommentListCreateApiView.as_view(),
        name="api_comments_list_create",
    ),
    path(
        "posts/<int:post_pk>/comments/<int:comment_pk>/",
        CommentDetailApiView.as_view(),
        name="api_comment_detail",
    ),
    path(
        "posts/<int:post_pk>/comments/<int:comment_pk>/like/",
        CommentLikeUnlikeApiView.as_view({"post": "like"}),
        name="api_comment_like",
    ),
    path(
        "posts/<int:post_pk>/comments/<int:comment_pk>/unlike/",
        CommentLikeUnlikeApiView.as_view({"post": "unlike"}),
        name="api_comment_unlike",
    ),
    path(
        "posts/<int:post_pk>/comments/<int:comment_pk>/fans/",
        CommentLikeUnlikeApiView.as_view({"get": "fans"}),
        name="api_comment_fans",
    ),
]
