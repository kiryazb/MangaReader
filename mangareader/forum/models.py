from django.db import models
from django.utils.text import slugify

from user.models import CustomUser


class Topic(models.Model):
    title = models.CharField(max_length=250)
    text = models.TextField()
    Author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.topic_slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class TopicComment(models.Model):
    text = models.TextField()
    topic = models.SlugField(max_length=255, default='null')
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.text
