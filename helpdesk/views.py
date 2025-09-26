from rest_framework import viewsets, permissions, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ticket
from .serializers import TicketSerializer, RegisterSerializer, UserSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

######Ticket######
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

######Register######
class RegisterView(generics.CreateAPIView):
    serializer_class= RegisterSerializer
    permission_classes= [permissions.AllowAny]


######Login######
class LoginView(APIView):
    permission_classes= [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password= request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return Response({"message": "Login Successful"})
        else:
            return Response({"message": "InValid Credentials"}, status=400)


######Logout######
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out Succesfully"})
    




        

