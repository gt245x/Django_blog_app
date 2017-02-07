from django.contrib import admin

# Register your models here.
from .models import Blog


class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'timeposted', 'updated']
    list_display_links = ['timeposted']
    list_editable = ['title']
    list_filter = ['updated', 'timeposted']
    search_fields = ['title', 'content']


    class Meta:
        model = Blog






admin.site.register(Blog, PostModelAdmin)