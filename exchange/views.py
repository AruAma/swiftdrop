from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from .models import Message, File
from django.db.models import Q
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm

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
    return render(request, 'exchange/profile.html', {'form': form})


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

@csrf_protect
def login_view(request):
    message = ""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('messages')
        else:
            message = "Login failed. Please check your credentials."
    else:
        form = AuthenticationForm()
    return render(request, 'exchange/login.html', {'form': form, 'message': message})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def messages_view(request):
    error = ""
    if request.method == 'POST':
        recipient_username = request.POST.get('recipient')
        content = request.POST.get('content')
        try:
            recipient = User.objects.get(username=recipient_username)
            Message.objects.create(sender=request.user, recipient=recipient, content=content)
        except User.DoesNotExist:
            error = "Recipient does not exist."
    messages = Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).select_related('sender', 'recipient').order_by('-timestamp')
    return render(request, 'exchange/messages.html', {'messages': messages, 'error': error})

@login_required
def files_view(request):
    error = ""
    if request.method == 'POST':
        recipient_username = request.POST.get('recipient')
        uploaded_file = request.FILES.get('file')
        try:
            recipient = User.objects.get(username=recipient_username)
            File.objects.create(uploader=request.user, recipient=recipient, file=uploaded_file)
        except User.DoesNotExist:
            error = "Recipient does not exist."
    files = File.objects.filter(Q(uploader=request.user) | Q(recipient=request.user)).select_related('uploader', 'recipient').order_by('-uploaded_at')
    return render(request, 'exchange/files.html', {'files': files, 'error': error})

def root_redirect(request):
    return redirect('login')

def home_view(request):
    return render(request, 'exchange/home.html')
