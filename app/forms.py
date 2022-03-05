from turtle import title
from django import forms
from mdeditor.fields import MDTextFormField

class PostForm(forms.Form):
    title = forms.CharField(max_length=30,label="タイトル")
    content = MDTextFormField()
   


