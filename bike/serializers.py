# 자전거 등록, 조회 과정 기능 구현
# bike/serializers.py

from django.contrib.auth.models import User  # User 모델 불러오기
from django.contrib.auth.password_validation import validate_password  # django의 기본 pw 검증 도구

from django.contrib.auth import authenticate
# django의 기본 authenticate 함수,
# 우리가 설정한 DefaultAuthBackend인 TokenAuth방식으로 유저를 인증해줌

from rest_framework import serializers
from rest_framework.authtoken.models import Token  # Token 모델
from rest_framework.validators import UniqueValidator  # 중복 방지를 위한 검증 도구

from .models import Component, Bike     # 부품, 자전거 모델


# 자전거 등록 시리얼라이저
# 자전거 등록 api 접근은 관리자에게만 허용됨 (추후 구현 예정)
class RegisterSerializer(serializers.ModelSerializer):
    frame_number = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Bike.objects.all())],  # 차대번호 중복 검사
    )
    image = serializers.ImageField(required=False, allow_null=True)     # image 필드 비워두는 것 허용
    current_pos = serializers.CharField(required=False)
    username = serializers.CharField(write_only=True)   # username
    registration_hash = serializers.CharField(required=False)


    class Meta:
        model = Bike
        exclude = ['user']
        # fields = ('username', 'manufacture_year', 'nickname', 'manufacturer', 'model', 'frame_number', 'weight',
        #          'registration_hash', 'registration_date', 'purchase_date', 'image', 'is_stolen', 'current_pos')

    def create(self, validated_data):
        # CREATE 요청, 자전거 생성 (블록체인 w3 API 요청 통해서 등록번호 생성 후 성공 시 DB 저장)
        # ----------- 여기서 WEb3 로직 실행----------------------------------- ##
        try:
            # registration_hash =
            pass
        except Exception as e:
            # raise serializers.ValidationError("blockchain error")
            pass
        # ---------------------------------------------------------------- ##
        username = validated_data.pop('username')
        try:
            user = User.objects.get(username=username)
            registration_hash = validated_data['frame_number']+'hash123'.upper()
        except User.DoesNotExist:
            raise serializers.ValidationError({'usernmae': 'User does not exist'})

        bike = Bike(user=user, registration_hash=registration_hash, **validated_data)
        bike.save()
        return bike


# 자전거 수정 API 시리얼라이저
# 별명, 무게, 이미지, 도난상태, 도난위치만 수정 가능!
class BikeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ('nickname', 'weight', 'image', 'is_stolen', 'current_pos')

    def update(self, instance, validated_data):
        # ----------- Web3 로직 추가 ------------- #
        # pass
        # -------------------------------------- #
        return super().update(instance, validated_data)


# 전체 정보 자전거 조회 시리얼라이저 (소유자)
class BikeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = '__all__'


# 일부 정보 조회용 시리얼라이저 (일반인 - 개인정보와 보험내역을 제외 조회)
class BikePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        exclude = ['user', 'nickname', 'current_pos']
        # fields = ['model', 'manufacturer', 'is_stolen']      # 추가 예정


# ToDo: 블록체인 보험, 수리 내역 추가 API 작성 필요
# ToDo: 블록체인 소유자 이전 API 작성 필요


# 자전거 목록 조회 시리얼라이저
class BikeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = '__all__'


# 부품 조회 시리얼라이저
class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'

