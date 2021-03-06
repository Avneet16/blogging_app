from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone

from my_site.forms import PostForm, CommentForm, UserForm
from django.contrib.auth.decorators import login_required
from .models import Post,Comment


# Create your views here.
def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    stuff_for_frontend={'posts': posts}
    return render(request,'my_site/post_list.html',stuff_for_frontend)

def post_detail(request,pk):
    post=get_object_or_404(Post, pk=pk)
    stuff_for_frontend = {'post': post}
    return render(request,'my_site/post_detail.html',stuff_for_frontend)

@login_required
def post_new(request):
    if request.method =='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form=PostForm()
        stuff_for_frontend={'form': form}
    return render(request,'my_site/post_edit.html',stuff_for_frontend)

@login_required
def post_edit(request,pk):
    global stuff_for_frontend
    post=get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            post=form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm(instance=post)
        stuff_for_frontend = {'form': form,'post':post}
    return render(request,'my_site/post_edit.html',stuff_for_frontend)

@login_required
def post_delete(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.delete()
    return redirect('/',pk=pk)

@login_required
def post_draft(request):
    post=Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    stuff_for_frontend = {'posts':post}
    return render(request,'my_site/post_draft.html',stuff_for_frontend)

@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def add_comment(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.author = request.user
            comment.post=post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render(request,'my_site/add_comment.html',{'form':form})

@login_required
def remove_comment(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.delete()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def approve_comment(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'my_site/signup.html', {'form': form})

