from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message, File

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('sender', 'timestamp')

class FileSerializer(serializers.ModelSerializer):
    def validate_file(self, value):
        if value.size > 10*1024*1024:
            raise serializers.ValidationError("File too large (max 10MB)")
        return value

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
