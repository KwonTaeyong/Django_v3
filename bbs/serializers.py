from rest_framework import serializers
from .models import Post


class Post_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'author': {'read_only': True},
            "views": {'read_only': True},
        }
