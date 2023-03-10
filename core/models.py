from django.db import models

class Post(models.Model):
    tag = models.CharField(max_length=55, verbose_name='Тэг')
    date = models.DateTimeField(verbose_name='Дата')
    post_id = models.IntegerField(default=0)
    photo = models.CharField(max_length=255,default=None)
    content = models.TextField(verbose_name='Текст поста')
    
