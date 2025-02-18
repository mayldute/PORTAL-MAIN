from django_filters import FilterSet, CharFilter, MultipleChoiceFilter, DateFromToRangeFilter
from django import forms 
from .models import Category

class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='iregex',
        label='Title'
    )

    category = MultipleChoiceFilter(
        field_name='category',
        choices=[(cat.id, cat.name) for cat in Category.objects.all()],
        widget=forms.Select,
        label='Category'
    )

    author = CharFilter(
        method='filter_by_author',
        label='Author'
    )

    date = DateFromToRangeFilter(
        field_name='create_time',
        lookup_expr='gt',
        widget=forms.widgets.MultiWidget(
        widgets=[forms.DateInput(attrs={'type': 'date'}), forms.DateInput(attrs={'type': 'date'})]
        ),
        label='Date'
    )

    def filter_by_author(self, queryset, name, value):
        return queryset.filter(
            author__user__first_name__iregex=value
        ) | queryset.filter(
            author__user__last_name__iregex=value
        )