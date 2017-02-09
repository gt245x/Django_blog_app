from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models.signals import pre_save

from django.utils.text import slugify

# Create your models here.
def upload_location(instance, filename):
    return "%s/%s" % (instance.slug, filename)


class Blog(models.Model):
    """Model for the Blog"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,
            null=True,
            blank=True,
            width_field = "width_field",
            height_field = "height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timeposted = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogs:detail', kwargs={'slug':self.slug})

    def get_editable_url(self):
        return reverse('blogs:update', kwargs={'slug':self.slug})

    def get_deletable_url(self):
        return reverse('blogs:delete', kwargs={'slug':self.slug})

    @property
    def image_url(self):
        if self.image and hasattr(self.image,'url'):
            return self.image.url


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Blog.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug = new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug=create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Blog)