from django.db import models # type: ignore
from django.contrib.auth.models import User

class Source(models.Model):
    name = models.CharField(max_length=100)
    domain = models.URLField()
    favicon = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=300)
    url = models.URLField(unique=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    content = models.TextField()
    summary = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=[(1, "Upvote"), (-1, "Downvote")])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')

    def __str__(self):
        return f"{self.user.username} voted {self.value} on {self.article.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"