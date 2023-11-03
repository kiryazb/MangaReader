from django.db import models

from django.urls import reverse


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


class Imprint(models.Model):
    name = models.CharField(max_length=50, help_text='imprint of work')

    def __str__(self):
        return f'{self.name}'


class Work(models.Model):
    title = models.CharField(max_length=200, null=True, unique=True)
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

    chapter_count = models.IntegerField()

    def get_absolute_url(self):
        return reverse('work-detail', args=[str(self.title)])

    def save(self, *args, **kwargs):
        # Удаление пробелов из значения поля name перед сохранением
        self.title = self.title.replace(" ", "_")
        super(Work, self).save(*args, **kwargs)

