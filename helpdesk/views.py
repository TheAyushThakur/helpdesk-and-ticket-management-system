from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ticket
from .serializers import TicketSerializer

# Create your views here.

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all() 
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'status', 'priority', 'assigned_to']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Ticket.objects.all()    
        profile = user.profile
        if profile.role == 'agent':
            return Ticket.objects.filter(assigned_to = user)
        return Ticket.objects.filter(created_by = user)
    
    def perform_create(self, serializer):
        serializer.save(created_by =self.request.user)


        

