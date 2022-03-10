from json import load
from operator import mod
from statistics import mode
from unicodedata import category, name
from django.db import models
from django.conf import settings
from django.utils import timezone
from mdeditor.fields import MDTextField

class Category(models.Model):
    name = models.CharField("カテゴリ",max_length=20)
    def __str__(self):
        return self.name

class Post(models.Model):
    auther  = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title   = models.CharField("タイトル",max_length=50)
    category = models.ForeignKey(Category,verbose_name="カテゴリ",on_delete=models.PROTECT)
    subtitle = models.CharField("サブタイトル",max_length=100)
    image   = models.ImageField(upload_to="images", verbose_name="画像",null=True, blank=True)
    content = MDTextField()
    created = models.DateTimeField("作成日",default=timezone.now)
    
    def __str__(self):
        return self.title
