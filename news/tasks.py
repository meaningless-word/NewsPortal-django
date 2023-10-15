from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

from news.management.commands.runapscheduler import my_job
from news.models import Post


@shared_task
def task_notification(post_id):
    post = Post.objects.get(id=post_id)
    subscribers = User.objects.filter(categories__in=post.categories.all()).values_list('email', flat=True)
    print(subscribers)

    subject = f'Новая публикация в категориях {", ".join(post.categories.all().values_list("name", flat=True))}'

    text_content = (
        f'{post.title}\n'
        f'{post.preview()}\n\n'
        f'доступна по ссылке: {settings.SITE_URL}{post.get_absolute_url()}'
    )

    html_content = (
        f'<h3>Добавлена <a href="{settings.SITE_URL}{post.get_absolute_url()}">публикация</a></h3>'
        f'<h4>{post.title}</h4>'
        f'<p>{post.preview()}</p>'
    )

    for subscriber in subscribers:
        msg = EmailMultiAlternatives(subject, text_content, None, [subscriber])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def task_weekly_sending():
    my_job()
