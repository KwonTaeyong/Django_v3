from rest_framework import serializers
from .models import User


class EmailSignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password")

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate(self, data):
        password = data['password']
        password2 = data['password2']
        # password와 password2 필드가 일치하는지 검사
        if password != password2:
            raise serializers.ValidationError("확인 비밀번호가 일치하지 않습니다.")

        if len(password) < 8:
            raise serializers.ValidationError("비밀번호는 최소 8자리 이상이어야 합니다..")

        special_characters = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~"
        if not any(char in special_characters for char in data['password']):
            raise serializers.ValidationError("비밀번호에는 적어도 하나 이상의 특수 문자가 포함되어야 합니다.")

        return data

    def create(self, validated_data):
        validated_data.pop('password2', None)
        user = User.objects.create(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class EmailLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = (
            'last_login',
            'is_staff',
            'first_name',
            'last_name',
            'is_active',
            'date_joined',
            'email'
        )
