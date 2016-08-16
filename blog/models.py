from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset() \
            .filter(status='published')


class NamedModel(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=250)


class TimeStampedModel(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Post(TimeStampedModel):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish',
                            allow_unicode=True)
    author = models.ForeignKey(User, related_name="posts")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='draft')

    class Meta:
        ordering = ('-publish',)

    def get_absolute_url(self):
        self.reverse = reverse('blog:post_detail',
                               args=[self.publish.year,
                                     self.publish.strftime('%m'),
                                     self.publish.strftime('%d'),
                                     self.slug])
        return self.reverse

    def __str__(self):
        return self.title
