from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from NewsPaper.NewsPaper.models import Article


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Добро пожаловать!',
            f'Здравствуйте, {instance.first_name if instance.first_name else "пользователь"}! Спасибо за регистрацию.',
            'admin@yourdomain.com',
            [instance.email],
            fail_silently=False,
        )

@receiver(post_save, sender=Article)
def notify_subscribers_on_new_article(sender, instance, created, **kwargs):
    if created:
        category = instance.category
        subscribers = category.subscriptions.all()
        for sub in subscribers:
            send_mail(
                f'Новая статья в категории {category.name}',
                f'''В категории "{category.name}" появилась новая статья: {instance.title}
            Краткое содержание:
            {instance.summary}

            Читать полностью: http://news_list.html/news/{instance.id}/
            ''',
                'no-reply@yourdomain.com',
                [sub.email],
                fail_silently=False,
            )