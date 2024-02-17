import django_filters
from django import forms
from .models import Testbed

class YourModelFilter(django_filters.FilterSet):
    dropdown_option1 = django_filters.ChoiceFilter(
        choices=[('all', 'all'), ('free', 'free'), ('used', 'notfree')],
        label='Usage',
        empty_label='all',
        method='filter_dropdown_option1'
    )
    
    dropdown_option2 = django_filters.ChoiceFilter(
        choices=[('latest', 'latest'), ('oldest', 'oldest')],
        label='Date',
        empty_label='oldest',
        method='filter_dropdown_option2'
    )

    class Meta:
        model = Testbed
        fields = ['dropdown_option1','dropdown_option2']

    def filter_dropdown_option1(self, queryset, name, value):
        if value == "all":
            return queryset
        return queryset.filter(usage=value)



    def filter_dropdown_option2(self, queryset, name, value):
        if value == "latest":
            return queryset.order_by('-date_posted')
        return queryset.order_by('date_posted')