from django.contrib import admin
from .models import Profile, Ticket
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display= ('user', 'role')
    search_fields = ('user__username', 'role')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display= ('title', 'status', 'priority', 'created_by', 'assigned_to', 'created_at')
    list_filter = ('priority', 'status')
    search_fields = ('title', 'priority', 'status', 'assigned_to')
