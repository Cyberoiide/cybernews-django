from django.shortcuts import render, redirect
from .models import Article, Comment
from .forms import CommentForm

def home(request):
    articles = Article.objects.select_related("source").order_by("-created_at")[:20]
    return render(request, "index.html", {"articles": articles})

def article_detail(request, article_id):
    article = Article.objects.get(id=article_id)
    comments = Comment.objects.filter(article=article, parent__isnull=True).order_by('-created_at')

    form = CommentForm()

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.article = article
            new_comment.save()
            return redirect('article_detail', pk=article.pk)

    return render(request, 'article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form
    })
