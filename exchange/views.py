from rest_framework import viewsets, generics, permissions
from django.db.models import Q
from .models import Message, File
from .serializers import MessageSerializer, FileSerializer, RegisterSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User

# api_views.py
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(sender=user) | Q(recipient=user))

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return File.objects.filter(Q(uploader=user) | Q(recipient=user))

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)

class RegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

@csrf_protect
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'exchange/register.html', {'form': form})

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('messages')
    else:
        form = AuthenticationForm()
    return render(request, 'exchange/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# views.py (for HTML views)
@login_required
def messages_view(request):
    if request.method == 'POST':
        recipient_username = request.POST.get('recipient')
        content = request.POST.get('content')
        try:
            recipient = User.objects.get(username=recipient_username)
            Message.objects.create(sender=request.user, recipient=recipient, content=content)
        except User.DoesNotExist:
            pass
    messages = Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).order_by('-timestamp')
    return render(request, 'exchange/messages.html', {'messages': messages})

@login_required
def files_view(request):
    if request.method == 'POST':
        recipient_username = request.POST.get('recipient')
        uploaded_file = request.FILES.get('file')
        try:
            recipient = User.objects.get(username=recipient_username)
            File.objects.create(uploader=request.user, recipient=recipient, file=uploaded_file)
        except User.DoesNotExist:
            pass
    files = File.objects.filter(Q(uploader=request.user) | Q(recipient=request.user)).order_by('-uploaded_at')
    return render(request, 'exchange/files.html', {'files': files})


# Redirect root to login
def root_redirect(request):
    return redirect('login')

def home_view(request):
    return render(request, 'exchange/home.html')
