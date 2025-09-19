from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Favorite, Like, Post
from .serializers import FavoriteSerializer, LikeSerializer, ReportSerializer


class PostLikeAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def post(self, request, post_id):
        """Like a post using serializer"""
        post = generics.get_object_or_404(Post, id=post_id)
        serializer = self.get_serializer(data={})
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, user=request.user)
        return Response({"message": "좋아요에 추가되었습니다."}, status=status.HTTP_201_CREATED)

    def delete(self, request, post_id):
        """Unlike a post safely"""
        post = generics.get_object_or_404(Post, id=post_id)
        like = Like.objects.filter(user=request.user, post=post).first()
        if like:
            like.delete()
            return Response({"message": "좋아요에서 제거되었습니다."}, status=status.HTTP_200_OK)
        return Response({"message": "좋아요에 추가되어있지 않습니다."}, status=status.HTTP_404_NOT_FOUND)


class PostFavoriteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer

    def post(self, request, post_id):
        """Favorite a post using serializer"""
        post = generics.get_object_or_404(Post, id=post_id)
        serializer = self.get_serializer(data={})
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, user=request.user)

        return Response({"message": "찜하기에 추가되었습니다."}, status=status.HTTP_201_CREATED)

    def delete(self, request, post_id):
        """Unfavorite a post safely"""
        post = generics.get_object_or_404(Post, id=post_id)
        favorite = Favorite.objects.filter(user=request.user, post=post).first()
        if favorite:
            favorite.delete()
            return Response({"message": "찜하기에서 제거되었습니다."}, status=status.HTTP_200_OK)
        return Response({"message": "찜하기에 추가되어있지 않습니다."}, status=status.HTTP_404_NOT_FOUND)


class PostReportAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReportSerializer

    def post(self, request, post_id):
        """Report a post"""
        post = generics.get_object_or_404(Post, id=post_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response({"message": "신고가 접수되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
