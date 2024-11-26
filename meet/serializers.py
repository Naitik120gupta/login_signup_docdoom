from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# Registration Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number'),
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user:
            if not user.is_active:
                raise serializers.ValidationError("Account is disabled.")
            
            # Serialize user data manually
            user_data = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone_number": user.phone_number,
            }
            
            return {
                "user": user_data,
                "token": str(RefreshToken.for_user(user).access_token),
            }
        
        raise serializers.ValidationError("Invalid email or password.")

# Password Reset Serializer
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

    def save(self):
        # Implement password reset email logic here
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        # For example, send a password reset email with a token or link
        print(f"Password reset email sent to {email}.")  # Placeholder
