from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.urls import reverse
from django.utils.text import slugify

from user.models import CustomUser


class Type(models.Model):
    name = models.CharField(max_length=15, help_text='Enter type of work')

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    subscribers = models.IntegerField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        permissions = (("can_change_authors", "add/delete/change authors"),)


class Imprint(models.Model):
    name = models.CharField(max_length=50, help_text='imprint of work')

    def __str__(self):
        return f'{self.name}'


def get_upload_path(instance, filename):
    return f'chapters_scans/{instance.work.slug}/chapter_{instance.chapter}/{filename}'


class Chapter(models.Model):
    title = models.CharField(max_length=50)
    chapter = models.IntegerField(default=0)
    work = models.ForeignKey('Work', related_name='chapters', on_delete=models.CASCADE)
    image = models.FileField(upload_to=get_upload_path)

    def __str__(self):
        return f'{self.title}'


@receiver(post_save, sender=Chapter)
def create_or_update_work(sender, instance, **kwargs):
    if kwargs.get('created', False):
        instance.work.chapter.add(instance)


class Work(models.Model):
    title = models.CharField(max_length=200, unique=True, null=True)
    slug = models.SlugField(max_length=255, null=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    release_year = models.IntegerField()

    WORK_STATUS = (
        ('f', 'freeze'),
        ('comp', 'complete'),
        ('cont', 'continue'),
    )

    work_status = models.CharField(max_length=4, choices=WORK_STATUS, default='f', help_text='work status')

    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    imprint = models.ManyToManyField(Imprint)

    age_rating = models.IntegerField()

    chapter = models.ManyToManyField(Chapter, related_name='works', blank=True)

    def get_absolute_url(self):
        return reverse('work-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Work, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    text = models.TextField()
    work = models.ForeignKey(Work, on_delete=models.SET_NULL, null=True)
    chapter = models.IntegerField()
    page = models.IntegerField()
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.text


class CommentWorkMainPage(models.Model):
    text = models.TextField()
    work = models.ForeignKey(Work, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, default=None)

    def __str__(self):
        return self.text
