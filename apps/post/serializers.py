from rest_framework import serializers
from .models import Post, PostLike, PostFavorite, PostReport


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"
        read_only_fields = ["user", "created_at"]


class PostFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostFavorite
        fields = "__all__"
        read_only_fields = ["user", "created_at"]


class PostReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReport
        fields = "__all__"
        read_only_fields = ["user", "created_at"]
