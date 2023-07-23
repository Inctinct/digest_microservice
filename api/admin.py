from django.contrib import admin
from .models import Subscription, Post, Digest

# Register your models here.

admin.site.register(Subscription)
admin.site.register(Post)
admin.site.register(Digest)
