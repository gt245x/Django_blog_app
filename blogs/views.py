from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader

from .models import Blog

# Create your views here.


def blog_list(request):
    queryset_list = Blog.objects.all()
    context = {
        "queryset" : queryset_list,
        "title" : "List"
    }
    return render(request, 'blogs/index.html', context)


def blog_create(request):
    return HttpResponse("This is the create page")


def blog_detail(request, id):
    return HttpResponse("This is the detail page")