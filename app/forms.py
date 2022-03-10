import email
from email import message
from turtle import title
from unicodedata import category, name
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

class ContactForm(forms.Form):
    name    = forms.CharField(max_length=30,label="名前")
    email   = forms.EmailField(max_length=30,label="メールアドレス")
    title   = forms.CharField(max_length=30, label="件名")
    message = forms.CharField(label="お問い合わせ内容",widget=forms.Textarea())
    
   

    
