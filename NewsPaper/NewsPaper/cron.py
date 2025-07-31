from django.utils import timezone
from django.core.mail import send_mail
from NewsPaper.NewsPaper.models import Article, Subscription

import datetime

def send_weekly_digest():
    one_week_ago = timezone.now() - datetime.timedelta(days=7)
    subs = Subscription.objects.all()

    for sub in subs:
        articles = Article.objects.filter(
            category=sub.category,
            created_at__gte=one_week_ago
        )
        if articles.exists():
            articles_list = ''
            for article in articles:
                articles_list += f'- {article.title}: http://news_list/news/{article.id}/\n'
            send_mail(
                f'Обзор новых статей за неделю в категории {sub.category.name}',
                f'Здравствуйте!\n\nЗа последнюю неделю в категории "{sub.category.name}" появились новые статьи:\n\n{articles_list}',
                'no-reply@yourdomain.com',
                [sub.email],
                fail_silently=False,
            )