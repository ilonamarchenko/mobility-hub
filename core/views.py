from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib import messages
from .forms import PostForm
from .models import Post
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.info(request, 'Будь ласка, заповніть свій профіль.')
            return redirect('edit_profile')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def home_view(request):
    try:
        profile = request.user.userprofile
    except ObjectDoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    return render(request, 'home.html', {'profile': profile})

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def edit_profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')  # нові перші
    university = request.GET.get('university')
    country = request.GET.get('country')
    program = request.GET.get('program')
    category = request.GET.get('category')

    if university:
        posts = posts.filter(university__icontains=university)
    if country:
        posts = posts.filter(country__icontains=country)
    if program:
        posts = posts.filter(exchange_program__icontains=program)
    if category:
        posts = posts.filter(hashtag_choice=category)
    return render(request, 'post_list.html', {'posts': posts})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_profile.html', {'form': form, 'post': post})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('post_list')

def all_posts_view(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})