from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect


from .models import Blog
from .forms import BlogForm

# Create your views here.


def blog_list(request):
    blog_list = Blog.objects.all()
    context = {
        "blog_list" : blog_list,
        "title" : "BlogPost"
    }
    return render(request, 'blogs/index.html', context)


def blog_create(request):
    form = BlogForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Successfully created the blog")
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            messages.error(request, "Blog was not successfully created")
    else:
        context = {
            "form" : form,
        }
        return render(request, 'blogs/create_blog.html', context)


def blog_detail(request, id):
    instance = get_object_or_404(Blog, id=id)
    context= {
        "title" : instance.title,
        "instance" : instance,
    }
    return render(request, 'blogs/blog_details.html', context)

def blog_update(request, id=None):
    instance = get_object_or_404(Blog, id=id)
    form  = BlogForm(request.POST or None, request.FILES or None, instance = instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully updated")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": instance.title,
        "instance" : instance,
        "form" : form,
    }
    return render(request, 'blogs/blog_update.html', context)

def blog_delete(request, id):
    instance = get_object_or_404(Blog, id=id)
    instance.delete()
    messages.success(request, "Successful on Delete")
    return redirect("blogs:list")