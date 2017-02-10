from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from urllib import quote_plus
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Blog
from .forms import BlogForm, UserForm
from django.db.models import Q

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json

# Create your views here.

def must_be_yours(func):
    """Decorator function to test ownership of object"""
    def check_and_call(request, *args, **kwargs):
        user = request.user
        print user.id
        slug = kwargs["slug"]
        blog = Blog.objects.get(slug=slug)
        if not (blog.user.id == request.user.id):
            return HttpResponse("""The blog was not authored by you!! You are
                not permitted. Create your own damn blog""" ,
                                content_type="application/json", status=403)
        return func(request, *args,  **kwargs)
    return check_and_call

def blog_list(request):
    """Renders all the blogs on the main page"""
    if not request.user.is_authenticated():
        return redirect("blogs:login_user")
    else:
        blog_list = Blog.objects.all().order_by("-timeposted")
        query = request.GET.get("q")
        if query:
            blog_list = blog_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
                ).distinct()
        paginator = Paginator(blog_list, 10) # Show 10 contacts per page
        page_request_var = 'page'
        page = request.GET.get(page_request_var)
        try:
            blogset = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            blogset = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            blogset = paginator.page(paginator.num_pages)

        context = {
            "blogset" : blogset,
            "title" : "BlogPost",
            "page_request_var" : page_request_var,
        }
        return render(request, 'blogs/index.html', context)


def blog_create(request):
    """Renders & handles creating new blog"""
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    form = BlogForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
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

def blog_detail(request, slug):
    """Renders each particular blog"""
    instance = get_object_or_404(Blog, slug=slug)
    share_string = quote_plus(instance.content)
    context= {
        "title" : instance.title,
        "instance" : instance,
        "share_string" : share_string,
    }
    return render(request, 'blogs/blog_details.html', context)

@must_be_yours
def blog_update(request, slug=None):
    """Handles editing & update of each blog"""
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    instance = get_object_or_404(Blog, slug=slug)
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

@must_be_yours
def blog_delete(request, slug):
    """Handles deleting of each blog"""
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    instance = get_object_or_404(Blog, slug=slug)
    instance.delete()
    messages.success(request, "Successful on Delete")
    return redirect("blogs:list")


def register(request):
    """Renders and handles registration for the blog page"""
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("blogs:list")
    context = {
        "form" : form,
    }
    return render(request, 'blogs/register.html', context)

def login_user(request):
    """Renders and handles login for the blog page"""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("blogs:list")
            else:
                context = {
                    "error_message":"Your account is disabled. Check with admin"
                }
                return render(request, 'blogs/login.html', context)
        else:
            context = {'error_message': 'Invalid login'}
            return render(request, 'blogs/login.html', context)
    return render(request, 'blogs/login.html')

def logout_user(request):
    """Renders and handles logout from the blog page"""
    logout(request)
    return redirect("blogs:list")


