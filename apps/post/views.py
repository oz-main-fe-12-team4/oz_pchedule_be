from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Post, PostLike, PostFavorite, PostReport
from .serializers import PostSerializer


# Post CRUD
class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Post.objects.filter(user=self.request.user)
        category = self.request.query_params.get("category")
        priority = self.request.query_params.get("priority")
        is_someday = self.request.query_params.get("is_someday")

        if category:
            queryset = queryset.filter(category=category)
        if priority:
            queryset = queryset.filter(priority=priority)
        if is_someday is not None:
            queryset = queryset.filter(is_someday=is_someday.lower() in ["true", "1"])

        return queryset


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


# 좋아요, 북마크, 신고
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    PostLike.objects.get_or_create(user=request.user, post=post)
    return Response({"message": "좋아요 완료"}, status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_favorite(request, pk):
    post = get_object_or_404(Post, pk=pk)
    PostFavorite.objects.get_or_create(user=request.user, post=post)
    return Response({"message": "북마크 완료"}, status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_report(request, pk):
    post = get_object_or_404(Post, pk=pk)
    reason = request.data.get("reason", "")
    PostReport.objects.create(user=request.user, post=post, reason=reason)
    return Response({"message": "신고 완료"}, status=200)
