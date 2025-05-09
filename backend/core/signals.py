from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Vote, Article

@receiver([post_save, post_delete], sender=Vote)
def update_article_score(sender, instance, **kwargs):
    article = instance.article
    votes = Vote.objects.filter(article=article)
    article.score = sum(v.value for v in votes)
    article.save() 