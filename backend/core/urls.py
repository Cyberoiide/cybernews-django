from django.urls import path, include
from .views import home, article_detail
from .api_views import ArticleCreateAPIView

urlpatterns = [
    path('', home, name='home'),
    path('article/<int:pk>/', article_detail, name='article_detail'),
    path('api/articles/', ArticleCreateAPIView.as_view()),
    path('users/', include('users.urls')),
]
