from celery import shared_task
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import send_mail
from .models import Post, UserCategorySubscription, PostCategory, Category
from django.conf import settings
from urllib.parse import urljoin
from django.utils import timezone
from datetime import timedelta

@shared_task
def notify_about_new_post(post_id, category):
    post = Post.objects.get(id=post_id)
    subscriptions = UserCategorySubscription.objects.filter(category__id__in=category)
    unique_users_email = set(subscription.user.email for subscription in subscriptions)
        
    for user_email in unique_users_email:
        post_url = urljoin(settings.BASE_URL, reverse('post_detail', kwargs={'pk': post.id}))
        unsubscribe_url = urljoin(settings.BASE_URL, reverse('cancel_subscription') + f"?email={user_email}")
            
        html_message = render_to_string('notify_about_new_post.html', {
            'title': post.title,
            'preview': post.preview(),
            'post_url': post_url,
            'unsubscribe_url': unsubscribe_url,
        })
            
        send_mail(
            subject=f'Вышла новая статья!',
            message='',
            html_message=html_message,
            recipient_list=[user_email],
            from_email=settings.DEFAULT_FROM_EMAIL,
            fail_silently=False,
            )
        
@shared_task
def weekly_notify():
    one_week_ago = timezone.now() - timedelta(days=7)
    recent_posts = Post.objects.filter(create_time__gte=one_week_ago)
    categories = Category.objects.filter(id__in=PostCategory.objects.filter(post__in=recent_posts).values('category_id')).distinct()
    subscriptions = UserCategorySubscription.objects.filter(category__in=categories)
    unique_user_email = set(subscription.user.email for subscription in subscriptions) 
    
    for user_email in unique_user_email:
        user_posts = [] 
        for subscription in subscriptions:
            category_id = subscription.category.id
            posts_for_category = recent_posts.filter(postcategory__category_id=category_id)
            user_posts.extend(posts_for_category)

        user_posts = sorted(set(user_posts), key=lambda post: post.create_time, reverse=True)
        
        html_message = render_to_string('weekly_notify_posts.html', {
            'user_posts': user_posts,
            })
        
        send_mail(
            subject=f'Статьи за последнюю неделю!',
            message='',
            html_message=html_message,
            recipient_list=[user_email],
            from_email=settings.DEFAULT_FROM_EMAIL,
            fail_silently=False,
        )
