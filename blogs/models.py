from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse


# Create your models here.
def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class Blog(models.Model):
    title = models.CharField(max_length=200)
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
        return reverse('blogs:detail', kwargs={'id':self.id})

    def get_editable_url(self):
        return reverse('blogs:update', kwargs={'id':self.id})

    def get_deletable_url(self):
        return reverse('blogs:delete', kwargs={'id':self.id})

    @property
    def image_url(self):
        if self.image and hasattr(self.image,'url'):
            return self.image.url


