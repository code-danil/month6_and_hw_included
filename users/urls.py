from django.urls import path
from users.views import RegistrationAPIView, AuthorizationAPIView, ConfirmUserAPIView
from users.google_oauth import GoogleloginApiView
from users.google_oauth_hw import GoogleAuthAPIView, GoogleCallbackAPIView

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('authorization/', AuthorizationAPIView.as_view()),
    path('confirm/', ConfirmUserAPIView.as_view()),
    path('google-login/', GoogleloginApiView.as_view()),
    path('google/', GoogleAuthAPIView.as_view()),
    path('google/callback/', GoogleCallbackAPIView.as_view()),
  
]
