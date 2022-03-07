from turtle import title
from unicodedata import category
from django import forms
from app.models import Category
from mdeditor.fields import MDTextFormField


class PostForm(forms.Form):
    category_data = Category.objects.all()
    category_choice = {}
    for category in category_data:
        category_choice[category] = category

    title = forms.CharField(max_length=50,label="タイトル")
    category = forms.ChoiceField(label="カテゴリ",widget=forms.Select,choices=list(category_choice.items()))
    subtitle = forms.CharField(max_length=100,label="サブタイトル")
    image = forms.ImageField(label="image画像",required=False)
    content = MDTextFormField()
    
   


