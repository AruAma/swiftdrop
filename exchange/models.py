from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.recipient} at {self.timestamp}"

class File(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploader = models.ForeignKey(User, related_name='uploaded_files', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_files', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} → {self.recipient}"
