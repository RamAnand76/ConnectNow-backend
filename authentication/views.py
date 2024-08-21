# authentication/views.py

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout, get_user_model
from .serializers import UserSerializer, LoginSerializer, InterestSerializer, MessageSerializer
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Interest, Message
import logging
from rest_framework import serializers
from .serializers import UserSerializer



logger = logging.getLogger(__name__)


User = get_user_model()


class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.data['username'],
                password=serializer.data['password']
            )
            if user:
                refresh = RefreshToken.for_user(user)
                login(request, user)
                update_last_login(None, user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class SendInterestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        sender = request.user
        receiver_username = request.data.get('receiver')
        message = request.data.get('message', '')

        if not receiver_username:
            return Response({'error': 'Receiver username is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return Response({'error': 'Receiver not found.'}, status=status.HTTP_404_NOT_FOUND)

        if receiver == sender:
            return Response({'error': 'You cannot send an interest to yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the interest object
        interest = Interest.objects.create(sender=sender, receiver=receiver, message=message)
        serializer = InterestSerializer(interest)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class ReceivedInterestsView(generics.ListAPIView):
    serializer_class = InterestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Interest.objects.filter(receiver=self.request.user, is_accepted=False, is_rejected=False)

class AcceptRejectInterestView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            interest = Interest.objects.get(pk=pk)
        except Interest.DoesNotExist:
            return Response({'error': 'Interest not found.'}, status=status.HTTP_404_NOT_FOUND)

        if interest.receiver != request.user:
            return Response({'error': 'You are not authorized to modify this interest.'}, status=status.HTTP_403_FORBIDDEN)

        is_accepted = request.data.get('is_accepted')
        is_rejected = request.data.get('is_rejected')

        if is_accepted and is_rejected:
            return Response({'error': 'Interest cannot be both accepted and rejected.'}, status=status.HTTP_400_BAD_REQUEST)

        if is_accepted:
            interest.is_accepted = True
            interest.is_rejected = False
        elif is_rejected:
            interest.is_rejected = True
            interest.is_accepted = False
        else:
            return Response({'error': 'Either is_accepted or is_rejected must be provided.'}, status=status.HTTP_400_BAD_REQUEST)

        interest.save()
        serializer = InterestSerializer(interest)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class AcceptedInterestListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        accepted_interests = Interest.objects.filter(sender=user, is_accepted=True)
        receiver_ids = accepted_interests.values_list('receiver_id', flat=True)
        return User.objects.filter(id__in=receiver_ids)



class ChatMessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sender = self.request.user
        receiver_username = self.kwargs['username']
        receiver = User.objects.get(username=receiver_username)
        return Message.objects.filter(sender=sender, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=sender)

    def perform_create(self, serializer):
        receiver_username = self.kwargs['username']
        receiver = User.objects.get(username=receiver_username)
        serializer.save(sender=self.request.user, receiver=receiver)