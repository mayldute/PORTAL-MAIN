from django.db import models
from django.urls import *
from django.contrib.auth.models import User
from django.core.cache import cache

TYPE = [
      ('AR', 'статья'),
      ('NW', 'новость')  
    ]

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default = 0)
    
    def update_rating(self):
        total_posts_rating = sum([post.rating for post in self.post_set.all()])
        total_comments_rating = sum([comment.rating for comment in Comment.objects.filter(post__author=self)])
        total_comments_on_posts_rating = sum([comment.rating for comment in Comment.objects.filter(post__author=self)])
        
        self.rating = total_posts_rating * 3 + total_comments_rating + total_comments_on_posts_rating
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    type = models.CharField(max_length=2, choices=TYPE, default = 'NW')
    create_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default = 0)
    
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')
    
    def preview(self):
        if len(self.text) > 20:
            if self.text[-1] in [',', ':', ';', '!', '?', '-', '(', ')', '*']:
                return f'{self.text[:19]}...'
            elif self.text[-1] == '.':
                return f'{self.text}..'
            else:
                return f'{self.text[:19]}...'
        else: 
            return f'{self.text}'
            
    def like(self):
        self.rating += 1
        self.save()
        
    def dislike(self):
        self.rating -= 1
        self.save()
        
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'product-{self.pk}')
    
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
class Comment(models.Model):
    text = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def like(self):
        self.rating += 1
        self.save()
        
    def dislike(self):
        self.rating -= 1
        self.save()
        
class UserCategorySubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)