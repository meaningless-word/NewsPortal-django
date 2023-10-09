from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

import config.settings as settings
from news.models import PostCategory, Post


def send_notification(post, subscribers):
    html_context = render_to_string(
        'news/post_created_email.html',
        {
            'text': post.preview(),
            'link': f'{settings.SITE_URL}/news/{post.pk}'
        }
    )

    for subscriber in subscribers:
        msg = EmailMultiAlternatives(
            subject=post.title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber],
        )

        msg.attach_alternative(html_context, 'text/html')
        msg.send()


@receiver(m2m_changed, sender=PostCategory)
def post_category_after_change(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        # subscribers = [s.email for c in instance.categories.all() for s in c.subscribers.all()]
        subscribers = User.objects.filter(categories__in=instance.categories.all()).values_list('email', flat=True)

        send_notification(instance, subscribers)


@receiver(post_save, sender=Post)
def post_after_create(instance, created, **kwargs):
    if not created:
        return

    subscribers = User.objects.filter(categories__in=instance.categories.all()).values_list('email', flat=True)

    subject = f'Новая публикация в категориях {", ".join(instance.categories.all().values_list("name", flat=True))}'

    text_content = (
        f'{instance.title}\n'
        f'{instance.preview()}\n\n'
        f'доступна по ссылке: {settings.SITE_URL}{instance.get_absolute_url()}'
    )

    html_content = (
        f'<h3>Добавлена <a href="{settings.SITE_URL}{instance.get_absolute_url()}">публикация</a></h3>'
        f'<h4>{instance.title}</h4>'
        f'<p>{instance.preview()}</p>'
    )

    for subscriber in subscribers:
        msg = EmailMultiAlternatives(subject, text_content, None, [subscriber])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
