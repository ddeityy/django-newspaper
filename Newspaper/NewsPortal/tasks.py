from datetime import datetime
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from NewsPortal.models import Category, Post


@shared_task
def send_weekly_mail():
    """#sends weekly mail with all posts of their subscribed categories"""
    for category in Category.objects.all():
        news_from_each_category = []
        last_week = datetime.now().isocalendar()[1] - 1
        for news in Post.objects.filter(post_category=category.id,
            creation_timedate__week=last_week).values(
                'pk',
                'title',
                'creation_timedate',
                'post_category__name'):
            date_format = news.get("creation_timedate").strftime("%m/%d/%Y")
            article =   (f'http://127.0.0.1:8000/news/{news.get("pk")}, {news.get("title")},'
                         f'Category: {news.get("post_category__name")}, Date: {date_format}')
            news_from_each_category.append(article)

    for subscriber in category.subscribers.all():
        html_content = render_to_string(
                'weekly.html', {'user': subscriber,
                                'text': news_from_each_category,
                                'category_name': category.name,
                                'last_week': last_week})
        msg = EmailMultiAlternatives(
        subject=f'Greetings, {subscriber.username}, here are the new articles from the last week.',
        from_email='',
        to=[subscriber.email]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
