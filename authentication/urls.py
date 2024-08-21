# authentication/urls.py

from django.urls import path
from .views import SignupView, LoginView, LogoutView
from .views import (
    UserListView, SendInterestView, ReceivedInterestsView, 
    AcceptRejectInterestView, ChatMessageListView, AcceptedInterestListView
)
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('interests/send/', SendInterestView.as_view(), name='send-interest'),
    path('interests/received/', ReceivedInterestsView.as_view(), name='received-interests'),
    path('interests/<int:pk>/respond/', AcceptRejectInterestView.as_view(), name='respond-interest'),
    path('chat/<str:username>/', ChatMessageListView.as_view(), name='chat-messages'),
    path('interests/accepted/', AcceptedInterestListView.as_view(), name='accepted_interests'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
