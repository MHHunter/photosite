from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Photo
from .forms import PhotoUploadForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('profile')
    else:
        form = PhotoUploadForm()
    return render(request, 'photos/upload_photo.html', {'form': form})


@login_required
def profile(request):
    photos = Photo.objects.filter(user=request.user)
    return render(request, 'photos/profile.html', {'photos': photos})


def public_photos(request):
    photos = Photo.objects.filter(visibility='public').order_by('-uploaded_at')[:9]
    return render(request, 'photos/public_photos.html', {'photos': photos})

def home(request):
    latest_photos = Photo.objects.filter(visibility='public').order_by('-uploaded_at')[:9]
    most_liked_photos = Photo.objects.filter(visibility='public').order_by('-likes')[:9]
    return render(request, 'photos/home.html', {
        'latest_photos': latest_photos,
        'most_liked_photos': most_liked_photos,
    })



@login_required
def like_photo(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    photo.likes += 1
    photo.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def search_users(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query)
    return render(request, 'photos/search_results.html', {'users': users, 'query': query})

def user_profile(request, username):
    user = User.objects.get(username=username)
    photos = Photo.objects.filter(user=user, visibility='public')
    return render(request, 'photos/user_profile.html', {'user': user, 'photos': photos})


@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id, user=request.user)
    if request.method == "POST":
        photo.delete()
        return redirect('home')  # or redirect to another page as needed
    return redirect('user_profile', username=request.user.username)