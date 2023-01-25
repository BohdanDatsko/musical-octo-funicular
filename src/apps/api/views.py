from django_filters import rest_framework as rfilters
from rest_framework import filters
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.api import services
from apps.api.serializers import (
    CommentCreateSerializer,
    PostCreateSerializer,
    CommentSerializer,
    PostSerializer,
    LikeSerializer,
    FanSerializer,
)
from apps.comments.models import Comment
from apps.posts.models import Post
from apps.reactions.models import Like


class PostListCreateApiView(generics.ListCreateAPIView):
    """
        PostListCreateApiView.
        Users can see all posts.
        Authorized users can also add new posts
    """

    queryset = Post.objects.all()
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ["title", "pub_date"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostSerializer
        else:
            return PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """
        PostDetailApiView.
        Authorized users can update or delete their posts
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsPostOwnerOrAdmin]
    lookup_field = "pk"
    lookup_url_kwarg = "post_pk"

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        request.data["owner"] = self.request.user.id
        response = super().update(request, *args, **kwargs)

        return response


class CommentListCreateApiView(generics.ListCreateAPIView):
    """
        CommentListCreateApiView.
        Users can see all post's comments.
        Authorized users can also add new comments to posts
    """

    queryset = Comment.objects.all()
    filter_backends = [filters.OrderingFilter, rfilters.DjangoFilterBackend]
    filterset_fields = ("post",)
    ordering_fields = ["post"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer
        else:
            return CommentCreateSerializer

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get("post_pk", None))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, post_id=self.kwargs.get("post_pk", None))


class CommentDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """
        CommentDetail.
        Authorized users can update or delete their comments
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "pk"
    lookup_url_kwarg = "comment_pk"

    def get_queryset(self):
        return Comment.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        request.data["owner"] = self.request.user.id
        response = super().update(request, *args, **kwargs)

        return response


class PostLikeUnlikeApiView(GenericViewSet, generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    lookup_field = "pk"
    lookup_url_kwarg = "post_pk"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Post.objects.filter(id=self.kwargs.get("post_pk", None))

    @action(methods=["POST"], detail=True)
    def like(self, request, **kwargs):
        """
        Likes "obj".
        """
        obj = self.get_object()
        services.add_like(obj, request.user)

        return Response(f'You have just liked "{obj}"')

    @action(methods=["POST"], detail=True)
    def unlike(self, request, **kwargs):
        """
        Remove like from "obj".
        """
        obj = self.get_object()
        services.remove_like(obj, request.user)

        return Response(f'You have just removed your like from "{obj}"')

    @action(detail=False)
    def fans(self, request, **kwargs):
        """
        Get all users which have liked "obj".
        """
        obj = self.get_object()
        fans = services.get_fans(obj)
        serializer = FanSerializer(fans, many=True)

        return Response(serializer.data)


class CommentLikeUnlikeApiView(GenericViewSet, generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    lookup_field = "pk"
    lookup_url_kwarg = "comment_pk"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Comment.objects.filter(id=self.kwargs.get("comment_pk", None))

    @action(methods=["POST"], detail=True)
    def like(self, request, **kwargs):
        """
        Likes "obj".
        """
        obj = self.get_object()
        services.add_like(obj, request.user)

        return Response(f'You have just liked "{obj}"')

    @action(methods=["POST"], detail=True)
    def unlike(self, request, **kwargs):
        """
        Remove like from "obj".
        """
        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response(f'You have just removed your like from "{obj}"')

    @action(detail=False)
    def fans(self, request, **kwargs):
        """
        Get all users which have liked "obj".
        """
        obj = self.get_object()
        fans = services.get_fans(obj)
        serializer = FanSerializer(fans, many=True)

        return Response(serializer.data)
