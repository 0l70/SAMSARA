from rest_framework import serializers
from .models import Article, Comment

# 1. 댓글 Serializer
class CommentSerializer(serializers.ModelSerializer):
    # ▼▼▼ [핵심] user의 username(이름)을 'username'이라는 필드로 꺼내온다!
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('article', 'user', )


# 2. 게시글 Serializer
class ArticleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        # ▼▼▼ [이 줄이 없으면 100% 400 에러 납니다] ▼▼▼
        read_only_fields = ('user', )