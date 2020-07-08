import django_filters
from django_filters import DateFilter, CharFilter
from .models import *


class ArticleFilter(django_filters.FilterSet):
    # langue
    # language = CharFilter(field_name="language",label='Langue')
    # auther = CharFilter(field_name="auther", lookup_expr='gte',label='Auteur')
    # category = CharFilter(field_name="category", label='Catégorie')
    # sub_category = CharFilter(label='Sous-Catégorie')
    
    start_date = DateFilter(field_name="date_published", lookup_expr='gte', label='Date de debut :')
    end_date = DateFilter(field_name="date_published", lookup_expr='lte', label='Date de fin :')
    title = CharFilter(field_name="title", lookup_expr='icontains', label='Titre')
    description = CharFilter(field_name="description", lookup_expr='icontains', label='Description')

    class Meta:
        model = Article
        fields = [
            'language',
            'auther',
            'category',
            'sub_category',
            'title',
            'description', 
            'start_date', 
            'end_date',
        ]
        
        exclude = ['date_published', 'date_updated', 'likes', 'is_published']