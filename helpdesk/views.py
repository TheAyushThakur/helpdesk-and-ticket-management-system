from rest_framework import viewsets, permissions, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ticket, Comment
from .serializers import TicketSerializer, RegisterSerializer, UserSerializer, LoginSerializer, CommentSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import PermissionDenied

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

    def perform_update(self, serializer):
        user = self.request.user
        
        if 'assigned_to' in serializer.validated_data and not user.is_superuser:
            serializer.validated_data.pop('assigned_to')
        serializer.save()

######Register######
class RegisterView(generics.CreateAPIView):
    serializer_class= RegisterSerializer
    permission_classes= [permissions.AllowAny]


######Login######
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
            request_body= LoginSerializer,
            responses={200: "Login Successful", 400: "InValid Credentials"}
    )

    def post(self, request):
        serializer= LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"message": "Login successful"})
        return Response({"error": "Invalid credentials"}, status=400)

######Logout######
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out Succesfully"})
    

######Comment######

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Comment.objects.all()
        if user.profile.role == "agent":
            return Comment.objects.filter(ticket__assigned_to=user)
        return Comment.objects.filter(ticket__created_by=user)

    @swagger_auto_schema(
        request_body=CommentSerializer,
        responses={
            201: openapi.Response("Comment created successfully", CommentSerializer),
            400: "Invalid data"
        }
    )
    def create(self, request, *args, **kwargs):
        """Create a new comment on a ticket (agents only)"""
        user = request.user
        if user.profile.role != "agent":
            raise PermissionDenied("Only agents can add comments/updates.")
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
