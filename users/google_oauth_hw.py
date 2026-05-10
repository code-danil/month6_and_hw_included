import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


CustomUser = get_user_model()


class GoogleAuthAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        google_auth_url = (
            'https://accounts.google.com/o/oauth2/v2/auth?'
            f'client_id={settings.GOOGLE_CLIENT_ID}'
            f'&redirect_uri={settings.GOOGLE_REDIRECT_URI}'
            f'&response_type=code'
            f'&scope=openid email profile'
        )
        return Response({'google_auth_url': google_auth_url})
    

class GoogleCallbackAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.query_params.get('code')
        
        token_response = requests.post(
            'https://oauth2.googleapis.com/token',
            data={
                'code': code,
                'client_id': settings.GOOGLE_CLIENT_ID,
                'client_secret': settings.GOOGLE_CLIENT_SECRET,
                'redirect_uri': settings.GOOGLE_REDIRECT_URI,
                'grant_type': 'authorization_code',
            }
        )
        print(f'TOKEN RESPONSE: {token_response.text}')

        token_data = token_response.json()
        access_token = token_data.get('access_token')

        user_info = requests.get(
            'https://www.googleapis.com/oauth2/v2/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}
        ).json()
        
        email = user_info.get('email')
        first_name = user_info.get('given_name')
        last_name = user_info.get('family_name')

        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'is_active': True,

            }

        )

        if not created:
            user.is_active = True
            user.save()

        token, _ = Token.objects.get_or_create(user=user)

        return Response({'key': token.key})
    
    