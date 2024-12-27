import django_filters
from django.db.models import Q
from .models import Post


class ListSearchFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    contents = django_filters.CharFilter(field_name='contents', lookup_expr='icontains')

    class Meta:
        model = Post
        fields = []