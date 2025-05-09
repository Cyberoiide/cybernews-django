from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.models import Article, Vote, Comment

@login_required
def profile_view(request):
    votes = Vote.objects.filter(user=request.user).select_related('article').order_by('-created_at')
    comments = Comment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'users/profile.html', {
        'votes': votes,
        'comments': comments,
    })

@login_required
def favorites_view(request):
    favorites = Article.objects.filter(vote__user=request.user, vote__value=1).distinct()
    return render(request, 'users/favorites.html', {
        'favorites': favorites,
    })
