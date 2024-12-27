from rest_framework import serializers
from .models import List, Cart


class ListSerializer(serializers.ModelSerializer):
    is_in_cart = serializers.SerializerMethodField()

    class Meta:
        model = List
        fields = '__all__'

    def get_is_in_cart(self, obj):
        request = self.context.get('request', None)

        if request.user.is_authenticated:
            return Cart.objects.filter(user=request.user.id, gongo=obj).exists()
        else:
            return False


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}
