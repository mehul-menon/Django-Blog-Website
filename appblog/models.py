
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create post model
class Post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    date=models.DateTimeField(default=timezone.now)
    # dont use pantheses for timezone.now 
    author= models.ForeignKey(User,on_delete=models.CASCADE)
    # on delete tells the app what to do if the user deletes his account. In this case post is also deleted.
    likes=models.ManyToManyField(User,related_name='blog_post')
    # create dunder str(dunder means double underscore) method to tell Post method what to show in shell
    def __str__(self):
        return self.title
# to redirect after updating post or creating new post
    def get_absolute_url(self):
         return reverse('post-detail',kwargs={'pk':self.pk})
    def total_likes(self):
        return self.likes.count()