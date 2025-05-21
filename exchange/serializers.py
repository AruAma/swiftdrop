from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message, File, Profile

# --- Profile Serializer ---
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


# --- Message Serializer ---
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('sender', 'timestamp')


# --- File Serializer ---
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ('uploader', 'uploaded_at')

    def validate_file(self, value):
        max_size = 10 * 1024 * 1024  # 10 MB
        allowed_types = [
            'application/pdf', 'image/jpeg', 'image/png', 'image/gif',
            'application/zip', 'text/plain'
        ]

        if value.size > max_size:
            raise serializers.ValidationError("File too large (max 10MB).")
        content_type = getattr(value, 'content_type', None)
        if content_type and content_type not in allowed_types:
            raise serializers.ValidationError("Unsupported file type.")
        return value


# --- Registration Serializer ---
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user)  # Автоматически создаёт профиль
        return user
