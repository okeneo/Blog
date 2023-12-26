from account.models import UserProfile
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    username = serializers.CharField(required=True)
    password1 = serializers.CharField(style={"input_type": "password"}, required=True)
    password2 = serializers.CharField(style={"input_type": "password"}, required=True)

    class Meta:
        model = UserProfile
        fields = ["email", "username", "password1", "password2"]

    def validate_email(self, email):
        email = email.lower()
        try:
            UserProfile.objects.get(email=email)
            raise serializers.ValidationError(f"The email address '{email}' is already registered.")
        except UserProfile.DoesNotExist:
            return email

    def validate_username(self, username):
        try:
            UserProfile.objects.get(username=username)
            raise serializers.ValidationError(f"The username '{username}' is already registered.")
        except UserProfile.DoesNotExist:
            return username

    def validate(self, data):
        email = data.get("email")
        username = data.get("username")
        password1 = data.get("password1")
        password2 = data.get("password2")

        if not email:
            raise serializers.ValidationError("Email is required.")
        if not username:
            raise serializers.ValidationError("Username is required.")
        if not password1:
            raise serializers.ValidationError("Password is required.")
        if not password2:
            raise serializers.ValidationError("Confirmation password is required.")
        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")

        # Extra validation for email and username.
        self.validate_email(email)
        self.validate_username(username)

        return data

    def create(self, validated_data):
        email = validated_data.get("email")
        username = validated_data.get("username")
        password = validated_data.get("password1")

        user = UserProfile.objects.create(email=email, username=username)
        user.set_password(password)
        user.save()
        return user
