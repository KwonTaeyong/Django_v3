from .serializers import Post_Serializer
from .models import Post
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .filter import ListSearchFilter
from rest_framework.permissions import IsAuthenticated


class BbsList_View(generics.ListAPIView):
    serializer_class = Post_Serializer
    queryset = Post.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ListSearchFilter


class BbsPost_View(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Post_Serializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BbsDetail_View(generics.RetrieveAPIView):
    """
    요청 시 해당 포스트 views += 1
    """
    serializer_class = Post_Serializer
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1  # 조회 시 views 값을 1 증가
        instance.save(update_fields=['views'])  # 데이터베이스에 변경 사항 저장
        return self.retrieve(request, *args, **kwargs)
