from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Message, File, Profile
from .forms import MessageForm, FileForm, ProfileForm


# --- Home Redirect ---
def root_redirect(request):
    return redirect('login')

def home_view(request):
    return render(request, 'exchange/home.html')


# --- Register View ---
@csrf_protect
def register_view(request):
    message = ""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            message = "Registration failed. Please check the form."
    else:
        form = UserCreationForm()
    return render(request, 'exchange/register.html', {'form': form, 'message': message})


# --- Login View ---
@csrf_protect
def login_view(request):
    message = ""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('messages')
        else:
            message = "Login failed. Please check your credentials."
    else:
        form = AuthenticationForm()
    return render(request, 'exchange/login.html', {'form': form, 'message': message})


# --- Logout View ---
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# --- Profile View ---
@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'exchange/profile.html', {'form': form, 'profile': profile})


# --- Messages View ---
@login_required
def messages_view(request):
    error = ""
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('messages')
    else:
        form = MessageForm()

    messages = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).select_related('sender', 'recipient').order_by('-timestamp')

    return render(request, 'exchange/messages.html', {'form': form, 'messages': messages})


# --- Files View ---
@login_required
def files_view(request):
    error = ""
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.uploader = request.user
            file.save()
            return redirect('files')
    else:
        form = FileForm()

    files = File.objects.filter(
        Q(uploader=request.user) | Q(recipient=request.user)
    ).select_related('uploader', 'recipient').order_by('-uploaded_at')

    return render(request, 'exchange/files.html', {'form': form, 'files': files})
