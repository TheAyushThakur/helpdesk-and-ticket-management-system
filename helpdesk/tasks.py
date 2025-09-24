from celery import shared_task
from django.utils import timezone
from .models import Ticket
from django.core.mail import send_mail
from django.contrib.auth.models import User

@shared_task
def check_ticket_escalations():
    now = timezone.now()

    for ticket in Ticket.objects.filter(status='open'):
        age = (now-  ticket.created_at).total_seconds()
        if ticket.priority == 'high' and age > 3600:
            ticket.status= "escalated"
            ticket.save()
        elif ticket.priority == 'medium' and age > 14400:
            ticket.status = 'escalated'
            ticket.save()
        elif ticket.priority == 'low' and age > 86400:
            ticket.status = 'escalated'
            ticket.save()
        
        subject = f"[Escalated] Ticket: {ticket.title}"
        message = f"""
Your Ticket '{ticket.title}' has been escalated due to inactivity.

Details:
-Priority: {ticket.priority}
-Status: {ticket.status}
-Created at: {ticket.created_at.strftime('%Y-%m-%d %H:%M')}
"""
        recipients=[]

        if ticket.created_by.email:
            recipients.append(ticket.created_by.email)
        
        admins = User.objects.filter(is_superuser= True)
        recipients.extend([admin.email for admin in admins if admin.email])

        if recipients:
            send_mail(
                subject,
                message,
                "helpdesk@example.com",
                recipients,
                fail_silently=True,
            )

