from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.shortcuts import get_object_or_404, get_list_or_404

from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer

# ----------------------------------------------------------------
# 1. 게시글 목록 조회 (GET) / 게시글 생성 (POST)
# ----------------------------------------------------------------
@api_view(['GET', 'POST'])
def article_list(request):
    # [조회]
    if request.method == 'GET':
        articles = Article.objects.all()
        # many=True: 데이터가 여러 개일 때 필수
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    # [생성] - 로그인한 사람만
    elif request.method == 'POST':
        # 로그인 안 했으면 거절
        if not request.user.is_authenticated:
            return Response({'error': '로그인이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)
            
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # 작성자(user) 정보 추가해서 저장
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# ----------------------------------------------------------------
# 2. 게시글 상세 조회 (GET) / 삭제 (DELETE) / 수정 (PUT)
# ----------------------------------------------------------------
@api_view(['GET', 'DELETE', 'PUT'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    # [상세 조회]
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    # [삭제]
    elif request.method == 'DELETE':
        # 본인 확인
        if request.user == article.user:
            article.delete()
            return Response({'message': '삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    # [수정]
    elif request.method == 'PUT':
        if request.user == article.user:
            # partial=True: 일부 데이터만 수정 가능하게 허용
            serializer = ArticleSerializer(article, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        else:
            return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)


# ----------------------------------------------------------------
# 3. 댓글 생성 (POST)
# ----------------------------------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # 로그인 필수 설정
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    
    if serializer.is_valid(raise_exception=True):
        # 댓글 저장 시 게시글(article)과 작성자(user) 정보 함께 저장
        serializer.save(article=article, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ----------------------------------------------------------------
# 4. 댓글 삭제 (DELETE)
# ----------------------------------------------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    # 댓글 작성자 본인인지 확인
    if request.user == comment.user:
        comment.delete()
        return Response({'message': '삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

# ----------------------------------------------------------------
# 4. 댓글 상세 (삭제 DELETE / 수정 PUT)
# ----------------------------------------------------------------
@api_view(['DELETE', 'PUT']) # 👈 PUT 메서드 추가됨!
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_pk): # 👈 이름 변경 (delete -> detail)
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    # [삭제]
    if request.method == 'DELETE':
        # 댓글 작성자 본인인지 확인
        if request.user == comment.user:
            comment.delete()
            return Response({'message': '삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    # [수정] 👇 이 부분이 새로 추가된 기능입니다!
    elif request.method == 'PUT':
        if request.user == comment.user:
            # partial=True: 내용(content)만 보내도 수정되도록 허용
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        else:
            return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)