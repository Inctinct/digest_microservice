from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Subscription(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    source_name = models.CharField(max_length=255)

    def __str__(self):
        return self.source_name


class Post(models.Model):
    subscription_id = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    content = models.TextField()
    popularity = (
        models.PositiveIntegerField()
    )  # popularity was based on the number of views of posts
    sphere = models.CharField(max_length=100)


class Digest(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    posts_list = models.ManyToManyField(Post)
