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


# Create your views here.


def blog_list(request):
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
    instance = get_object_or_404(Blog, slug=slug)
    share_string = quote_plus(instance.content)
    context= {
        "title" : instance.title,
        "instance" : instance,
        "share_string" : share_string,
    }
    return render(request, 'blogs/blog_details.html', context)

def blog_update(request, slug=None):
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

def blog_delete(request, slug):
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    instance = get_object_or_404(Blog, slug=slug)
    instance.delete()
    messages.success(request, "Successful on Delete")
    return redirect("blogs:list")


def register(request):
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
    logout(request)
    return redirect("blogs:list")