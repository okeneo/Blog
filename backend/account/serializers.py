from account.models import UserProfile
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    # The email is validated by the EmailField email validator.
    email = serializers.EmailField(max_length=255, required=True)
    username = serializers.CharField(max_length=150, required=True)
    password1 = serializers.CharField(
        style={"input_type": "password"}, required=True, write_only=True
    )
    password2 = serializers.CharField(
        style={"input_type": "password"}, required=True, write_only=True
    )

    class Meta:
        model = UserProfile
        fields = [
            "email",
            "username",
            "password1",
            "password2",
        ]

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
            username_validator = UnicodeUsernameValidator()
            try:
                # Validate the username using the default User model username validator.
                username_validator(username)
            except ValueError as e:
                raise serializers.ValidationError(str(e))
            return username

    def validate_password1(self, password1):
        try:
            # Validate the password using the Django's built-in password validator.
            validate_password(password1)
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        return password1

    def validate(self, data):
        email = data.get("email")
        username = data.get("username")
        password1 = data.get("password1")
        password2 = data.get("password2")

        # Extra validation for email and username.
        self.validate_email(email)
        self.validate_username(username)
        self.validate_password1(password1)

        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        email = validated_data.get("email")
        username = validated_data.get("username")
        password = validated_data.get("password1")

        user = UserProfile.objects.create(email=email, username=username)
        user.set_password(password)
        user.save()
        return user


class UserProfilePublicSerializer(serializers.ModelSerializer):
    """The fields in this serializer represent data that can be viewed by anyone on the
    internet."""

    class Meta:
        model = UserProfile
        fields = [
            "username",
            "bio",
        ]


class UserProfilePrivateSerializer(serializers.ModelSerializer):
    """The fields in this serializer represent data that only the user of the associated
    account, or users with the admin role should have access to."""

    # TODO: Should we use this serializer for user account updates?

    class Meta:
        model = UserProfile
        fields = [
            "username",
            "bio",
            "email",
            "first_name",
            "last_name",
            "role",
        ]


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = [
            "password",
        ]
