from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from .models import Profile


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    password1 = serializers.CharField(
        style={"input_type": "password"}, required=True, write_only=True
    )
    password2 = serializers.CharField(
        style={"input_type": "password"}, required=True, write_only=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
        ]

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
            raise serializers.ValidationError(f"The username '{username}' is already registered.")
        except User.DoesNotExist:
            username_validator = UnicodeUsernameValidator()
            try:
                # Validate the username using the default User model username validator.
                username_validator(username)
            except ValueError as e:
                raise serializers.ValidationError(str(e))
            return username

    def validate_password1(self, password1):
        try:
            # Validate the password using Django's built-in password validator.
            validate_password(password1)
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        return password1

    def validate(self, data):
        password1 = data.get("password1")
        password2 = data.get("password2")

        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        username = validated_data.get("username")
        password = validated_data.get("password1")
        user = User.objects.create_user(username=username, password=password)

        return user


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    role = serializers.CharField(max_length=10, read_only=True)
    bio = serializers.CharField(max_length=500, allow_blank=True)

    class Meta:
        model = Profile
        fields = [
            "username",
            "role",
            "bio",
        ]

    def get_username(self, obj):
        return obj.user.username


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(allow_blank=True)
    first_name = serializers.CharField(max_length=150, allow_blank=True)
    last_name = serializers.CharField(max_length=150, allow_blank=True)
    password1 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "profile",
        ]

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
            raise serializers.ValidationError(f"The username '{username}' is already registered.")
        except User.DoesNotExist:
            username_validator = UnicodeUsernameValidator()
            try:
                # Validate the username using the default User model username validator.
                username_validator(username)
            except ValueError as e:
                raise serializers.ValidationError(str(e))
            return username

    def validate_password1(self, password1):
        try:
            # Validate the password using Django's built-in password validator.
            validate_password(password1)
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        return password1

    def validate(self, data):
        password1 = data.get("password1")
        password2 = data.get("password2")

        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def update(self, instance, validated_data):
        # Update User data.
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.irst_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)

        password = validated_data.get("password1")
        if password:
            instance.set_password(password)

        instance.save()

        # Update Profile data.
        profile_data = validated_data.pop("profile", None)
        profile = instance.profile
        if profile_data:
            profile.bio = profile_data.get("bio", profile.bio)
            profile.save()

        return instance
