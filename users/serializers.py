# 회원가입, 로그인 과정에 대한 기능 구현
# users/serializers.py

from django.contrib.auth.models import User  # User 모델 불러오기
from django.contrib.auth.password_validation import validate_password  # django의 기본 pw 검증 도구

from django.contrib.auth import authenticate
# django의 기본 authenticate 함수,
# 우리가 설정한 DefaultAuthBackend인 TokenAuth방식으로 유저를 인증해줌

from rest_framework import serializers
from rest_framework.authtoken.models import Token  # Token 모델
from rest_framework.validators import UniqueValidator  # 이메일 중복 방지를 위한 검증 도구

from .models import Profile     # 프로필 모델


# 회원가입 시리얼라이저
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],  # 이메일 중복 검사
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],  # 비밀번호 검증
    )
    password2 = serializers.CharField(  # 비밀번호 확인 필드
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')

    def validate(self, data):
        # password와 password2 일치 여부 확인
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return data

    def create(self, validated_data):
        # CREATE 요청에 대해 메서드 오버라이딩, 유저 생성 및 토큰 생성
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user


# 로그인 시리얼라이저
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user)    # 해당 유저의 토큰 불러오기
            return token
        raise serializers.ValidationError(  # 가입된 유저 없을 경우
            {"error": "Unable to log in with provided credentials."}
        )


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "birthday", "phone", "image")

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name
