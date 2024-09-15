from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
        print("Testing order of execution: validate_password1()")
        try:
            # Validate the password using Django's built-in password validator.
            validate_password(password1)
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        return password1

    def validate(self, data):
        print("Testing order of execution: validate()")
        password1 = data.get("password1")
        password2 = data.get("password2")

        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        username = validated_data.get("username")
        password = validated_data.get("password1")

        user = User(username=username)
        user.set_password(password)
        user.save()

        return user


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    bio = serializers.CharField(max_length=500, read_only=True)
    role = serializers.CharField(max_length=10, read_only=True)

    class Meta:
        model = Profile
        fields = [
            "username",
            "bio",
            "role",
        ]

    def get_username(self, obj):
        return obj.user.username

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Conditionally remove the 'user' field when it's nested inside UserSerializer.
        if "request" in self.context and isinstance(
            self.context["request"].parser_context["view"], UserSerializer
        ):
            representation.pop("username", None)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    password1 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    profile_data = ProfileSerializer()

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "profile_data",
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
        profile_data = validated_data.pop("profile_data")
        profile = instance.profile

        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.irst_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)

        password = validated_data.get("password1")
        if password:
            instance.set_password(password)

        instance.save()

        profile_data.bio = profile_data.get("bio")
        if profile_data.bio:
            profile.save()

        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """A custom serializer that adds 'username' to the payload of a JWT token."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token
