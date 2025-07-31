from django.shortcuts import render, get_object_or_404
from .models import News
from .tasks import notify_subscribers

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

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm

# Общие функции
def create_post(request, post_type):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.post_type = post_type
            post.save()
            return redirect('news_list' if post_type == Post.NEWS else 'articles_list')
    else:
        form = PostForm()
    context = {
        'form': form,
        'post_type': post_type,
    }

    def create_news_article(request, category):
        # Ваш текущий код
        if form.is_valid():
            news_article = form.save(commit=False)
            # Сохранение новости
            news_article.save()

            # Отправка уведомления подписчикам
            notify_subscribers.delay(news_article.id)

            return redirect('news_list')

    template_name = 'posts/create_post.html'
    return render(request, template_name, context)

def edit_post(request, pk, post_type):
    post = get_object_or_404(Post, pk=pk, post_type=post_type)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('news_list' if post_type == Post.NEWS else 'articles_list')
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
        'post': post,
        'post_type': post_type,
    }
    template_name = 'posts/edit_post.html'
    return render(request, template_name, context)

def delete_post(request, pk, post_type):
    post = get_object_or_404(Post, pk=pk, post_type=post_type)
    if request.method == 'POST':
        post.delete()
        return redirect('news_list' if post_type == Post.NEWS else 'articles_list')
    context = {
        'post': post,
        'post_type': post_type,
    }
    template_name = 'posts/delete_post.html'
    return render(request, template_name, context)

# views.py (добавьте)
def news_list(request):
    posts = Post.objects.filter(post_type=Post.NEWS).order_by('-created_at')
    return render(request, 'posts/list.html', {'posts': posts, 'title': 'Новости'})

def articles_list(request):
    posts = Post.objects.filter(post_type=Post.ARTICLE).order_by('-created_at')
    return render(request, 'posts/list.html', {'posts': posts, 'title': 'Статьи'})


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect

@login_required
def become_author(request):
    authors_group, _ = Group.objects.get_or_create(name='authors')
    request.user.groups.add(authors_group)
    return redirect('profile')  # или куда нужно

