from django_filters import rest_framework as filters
from app_lessons.models import LessonName


class LessonNameFilter(filters.FilterSet):
    lesson_category = filters.CharFilter(field_name='lesson_category__category_name', lookup_expr='icontains')

    class Meta:
        model = LessonName
        fields = ['lesson_category']