from rest_framework import generics, status
from .serializers import ListSerializer, CartSerializer
from .models import List, Cart
from django_filters.rest_framework import DjangoFilterBackend
from .filter import ListSearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class GongoListView(generics.ListAPIView):
    serializer_class = ListSerializer
    queryset = List.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ListSearchFilter


class GongoDetailView(generics.RetrieveAPIView):
    """
    요청 시 해당 공고 views += 1
    """
    serializer_class = ListSerializer
    queryset = List.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1  # 조회 시 views 값을 1 증가
        instance.save(update_fields=['views'])  # 데이터베이스에 변경 사항 저장
        return self.retrieve(request, *args, **kwargs)


class GongoUploadView(generics.CreateAPIView):
    serializer_class = ListSerializer


class AddToCartView(generics.CreateAPIView):
    """
    로그인(토큰) 필수
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def post(self, request, *args, **kwargs):
        # 사용자와 연관된 장바구니 항목이 있는지 확인
        cart_item = Cart.objects.filter(user=request.user, **request.data).first()
        if cart_item:
            # 항목이 이미 존재하면 삭제
            cart_item.delete()
            return Response({
                'message': 'Item removed from cart'
            }, status=status.HTTP_200_OK)
        else:
            # 존재하지 않으면 새로운 항목 생성
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartListView(generics.ListAPIView):
    """
    로그인(토큰) 필수
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ListSerializer

    def get_queryset(self):
        user = self.request.user
        carts = Cart.objects.filter(user=user.id)
        list_ids = carts.values_list('gongo', flat=True)
        return List.objects.filter(id__in=list_ids)


class GongoStatusView(generics.ListAPIView):
    serializer_class = ListSerializer
    queryset = List.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ListSearchFilter
