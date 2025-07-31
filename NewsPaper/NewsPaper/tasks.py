from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import send_mail
from NewsPaper.NewsPaper.models import Article

@shared_task
def notify_subscribers(news_article_id):
    news_article = Article.objects.get(id=news_article_id)
    subscribers = ['subscriber1@example.com', 'subscriber2@example.com']

    subject = f'Новая статья: {news_article.title}'
    message = f'{news_article.content}\n\nЧитать больше на нашем сайте.'

    send_mail(subject, message, 'from@example.com', subscribers)


@shared_task
def weekly_newsletter():
    # Получаем все новости за неделю
    news_articles = Article.objects.filter(created_at=datetime.now() - timedelta(days=7))
    if news_articles:
        subscribers = ['subscriber1@example.com', 'subscriber2@example.com']
        subject = 'Еженедельная рассылка с последними новостями'
        message = 'Вот последние новости:\n'

        for article in news_articles:
            message += f'{article.title}: {article.content}\n'

        send_mail(subject, message, 'from@example.com', subscribers)