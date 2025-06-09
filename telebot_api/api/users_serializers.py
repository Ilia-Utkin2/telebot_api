from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'username': {'error_messages': {'required': 'Поле имени пользователя обязательно.'}},
            'email': {'error_messages': {'required': 'Поле email обязательно.'}},
            'password': {'error_messages': {'required': 'Поле пароля обязательно.'}},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError(
                f"Пользователь с email '{value}' уже существует.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError(
                f"Пользователь с именем '{value}' уже существует.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        extra_kwargs = {
            'username': {'error_messages': {'required': 'Поле имени пользователя обязательно.'}},
            'email': {'error_messages': {'required': 'Поле email обязательно.'}},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise ValidationError(
                f"Пользователь с email '{value}' уже существует.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise ValidationError(
                f"Пользователь с именем '{value}' уже существует.")
        return value
