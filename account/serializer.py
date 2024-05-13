from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from .tasks import send_activation_code_celery

from account.utils import send_activation_code

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4, required=True)
    name = serializers.CharField()
    last_name = serializers.CharField()

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValueError(
                'Пользователь с таким email уже существует'
            )
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError(
                'Пароли не совпадают'
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_code_celery.delay(user.email, user.activation_code)
        return user


class ActivationSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    code = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        if not User.objects.filter(
            email=email, activation_code=code
        ).exists():
            raise serializers.ValidationError(
                'Пользователь не найден'
            )
        return attrs

    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(
            email=email
        ).exists():
            raise serializers.ValidationError(
                'Пользователь не найден'
            )
        return email

    def validate(self, attrs):
        request = self.context.get('request')
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(
                username=email,
                password=password,
                request=request
            )
            if not user:
                raise serializers.ValidationError(
                    'Не верный email или пароль'
                )
        else:
            raise serializers.ValidationError(
                'Email и пароль обязательны к заполнению'
            )
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=4, required=True)
    new_password = serializers.CharField(min_length=4, required=True)
    new_password_confirm = serializers.CharField(min_length=4, required=True)

    def validate_old_password(self, old_password):
        request = self.context.get('request')
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                'Введите правильный пароль'
            )
        return old_password

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')
        if new_password != new_password_confirm:
            raise ValueError(
                'Пароли не совпадают'
            )
        if old_password == new_password:
            raise serializers.ValidationError(
                'Пароли совпадают'
            )
        return attrs

    def set_new_password(self):
        new_password = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_password)
        user.save()

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email):
            raise serializers.ValidationError(
                'Такого пользователя нет'
            )
        return email

    def send_verification_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail(
            'Восстановление пароля',
            f'Ваш код восстановления: {user.create_activation_code}',
            'hotelo@gmail.com',
            [user.email]
        )


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if not User.objects.filter(email=email, activation_coe=code):
            raise serializers.ValidationError(
                'Пользователь не найден'
            )
        if password != password_confirm:
            raise serializers.ValidationError(
                'Пароли не совпадают'
            )
        return attrs

    def get_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
