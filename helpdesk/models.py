from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    Role_Choices=(
        ('user', 'User'),
        ('agent', 'Agent'),
        ('admin', 'Admin'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=Role_Choices, default='user')

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class Ticket(models.Model):
    Priority_Choices =(
        ('low', "Low"),
        ('medium', "Medium"),
        ('high', "High"),
    )

    Status_Choices =(
        ('open', "Open"),
        ('in-progress', "In Progress"),
        ('resolved', "Resolved"),
        ('closed', 'Closed'),
        ('escalated', 'Escalated'),
    )

    title = models.CharField(max_length=200)
    description= models.TextField()
    priority = models.CharField(max_length=10, choices=Priority_Choices, default="low")
    status = models.CharField(max_length=20, choices=Status_Choices, default="open")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title