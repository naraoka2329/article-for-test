from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='タイトル')
    text = models.TextField(verbose_name='本文')
    timestamp = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    
class Comment(models.Model):
    text = models.TextField('コメント')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField('投稿日', default=timezone.now)
    def __str__(self):
        return self.text