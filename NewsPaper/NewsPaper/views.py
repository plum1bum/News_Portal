from django.shortcuts import render, get_object_or_404
from .models import News

def news_list(request):
    articles = News.objects.all().order_by('-pub_date')
    return render(request, 'default.html', {
        'content_template': 'news_list.html',
        'articles': articles
    })

def news_detail(request, id):
    article = get_object_or_404(News, pk=id)
    return render(request, 'default.html', {
        'content_template': 'news_detail.html',
        'article': article
    })
