from json import load
from django.db import models
from django.conf import settings
from django.utils import timezone
from mdeditor.fields import MDTextField

class Post(models.Model):
    # auther  = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    # title   = models.CharField("タイトル",max_length=30)
    # image   = models.ImageField(upload_to="images", verbose_name="画像",null=True, blank=True)
    # content = models.TextField("本文")
    # created = models.DateTimeField("作成日",default=timezone.now)
    
    auther  = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title   = models.CharField("タイトル",max_length=30)
    content = MDTextField()
    created = models.DateTimeField("作成日",default=timezone.now)
    
    def __str__(self):
        return self.title

 