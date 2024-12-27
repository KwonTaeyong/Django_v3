import django_filters
from django.db.models import Q

from .models import List, Cart


class ListSearchFilter(django_filters.FilterSet):
    search_all = django_filters.CharFilter(method='filter_search')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    contents = django_filters.CharFilter(field_name='contents', lookup_expr='icontains')
    source = django_filters.CharFilter(field_name='sourceOrg', lookup_expr='icontains')

    class Meta:
        model = List
        fields = []

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(contents__icontains=value) |
            Q(sourceOrg__icontains=value)
        )