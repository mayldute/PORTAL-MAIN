from django_filters import FilterSet, CharFilter, DateFilter
from django import forms 

class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='iregex',
        label='Title'
    )
    author = CharFilter(
        method='filter_by_author',
        label='Author'
    )
    date = DateFilter(
        field_name='create_time',
        lookup_expr='gt',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Date'
    )

    def filter_by_author(self, queryset, name, value):
        return queryset.filter(
            author__user__first_name__iregex=value
        ) | queryset.filter(
            author__user__last_name__iregex=value
        )
