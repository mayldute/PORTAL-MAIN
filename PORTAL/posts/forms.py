from django import forms
from .models import Post, Category

class PostForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.SelectMultiple)
    class Meta:
        category_name = forms.CharField() 
        model = Post
        fields = [
            'title',
            'text',
            'category',
        ]