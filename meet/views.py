from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer, PasswordResetSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PasswordResetSerializer, SetNewPasswordSerializer

User = get_user_model()


# Password Reset API
class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            reset_link = request.build_absolute_uri(
                reverse('set_new_password') + f"?token={token}&email={email}"
            )
            # Send the email
            send_mail(
                subject="Password Reset Request",
                message=f"Click the link to reset your password: {reset_link}",
                from_email="no-reply@example.com",
                recipient_list=[email],
            )
            return Response({"message": "Password reset link sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Set New Password API
class SetNewPasswordView(APIView):
    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            try:
                user = User.objects.get(email=email)
                token_generator = PasswordResetTokenGenerator()
                if token_generator.check_token(user, token):
                    user.set_password(new_password)
                    user.save()
                    return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

