from account.models import UserProfile
from django.contrib.auth import authenticate
from rest_framework import serializers


class UserSignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    username = serializers.CharField(required=True)
    password1 = serializers.CharField(
        style={"input_type": "password"}, required=True, write_only=True
    )
    password2 = serializers.CharField(
        style={"input_type": "password"}, required=True, write_only=True
    )

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


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(
        style={"input_type": "password"}, required=True, write_only=True
    )

    class Meta:
        model = UserProfile
        fields = ["email", "username"]

    def validate(self, data):
        email = data.get("email", None)
        username = data.get("username", None)
        password = data.get("password")

        if email:
            user = authenticate(request=self.context.get("request"), email=email, password=password)
        elif username:
            user = authenticate(
                request=self.context.get("request"), username=username, password=password
            )
        else:
            raise serializers.ValidationError("Username and email were not provided.")

        if not user:
            raise serializers.ValidationError("Invalid login credentials.")

        data["user"] = user
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "role",
        )
