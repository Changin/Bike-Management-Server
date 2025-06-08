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
from users.models import Profile

import requests


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
        username = validated_data.pop('username')
        try:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            # registration_hash = validated_data['frame_number']+'hash123'.upper() # api 연동 전 테스트용

            # ------------------------------------------------- Web3 api 호출 -------- #
            # 블록체인 자전거 등록 url
            register_url = 'http://localhost:8080/blockchain/api/register_bicycle/'
            # post 요청 내용
            payload = {
                "frameNumber": validated_data['frame_number'],
                "manufacturer": validated_data['manufacturer'],
                "model": validated_data['model'],
                "purchaseDate": str(validated_data['purchase_date']).replace('-', ''),
                "manufactureYear": validated_data['manufacture_year'],
                "ownerId": username,  # 소유자 id
                "ownerName": user.last_name + " " + user.first_name,    # 소유자 이름
                "ownerRRNFront": profile.birthday,  # 주민번호 앞자리
                "ownerContact": profile.phone,  # 연락처
                "weight": validated_data['weight']
            }
            response = requests.post(url=register_url, json=payload)
            if response.status_code != 200:
                raise serializers.ValidationError("blockchain error")

            data = response.json()
            if data['status'] == "error":
                raise serializers.ValidationError(data['message'])

            # 등록번호 조회 api 호출
            hash_url = 'http://localhost:8080/blockchain/api/get_registration_hash/'
            hash_payload = {
                "frameNumber": validated_data['frame_number']
            }
            response = requests.post(url=hash_url, json=hash_payload)
            if response.status_code != 200:
                raise serializers.ValidationError("blockchain error")

            data = response.json()
            if data['status'] == "error":
                print('blockchain response error!')
                raise serializers.ValidationError(data['message'])

            registration_hash = data['registrationHash']

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
        # ToDo: 무게 변경 시 블록체인 api 호출 로직 추가 예정
        # 도난 여부 상태 변경 블록체인 호출
        if instance.is_stolen != validated_data['is_stolen']:
            url = 'http://localhost:8080/blockchain/api/report_stolen/'
            payload = {
                'registrationHash': instance.registration_hash,
                'isStolen': validated_data['is_stolen']
            }
            response = requests.post(url=url, json=payload)
            if response.status_code != 200:
                print('stolen report error!' + response.status_code)
                raise serializers.ValidationError("blockchain error")
        # -------------------------------------- #
        return super().update(instance, validated_data)


# 전체 정보 자전거 조회 시리얼라이저 (소유자)
class BikeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = '__all__'

    def to_representation(self, instance):
        # 보험/수리/튜닝/소모품 횟수 및 날짜
        # 소유자 변경 카운트/ 날짜
        rep = super().to_representation(instance)
        registration_hash = instance.registration_hash

        # 블록체인 api 호출
        repair_url = 'http://localhost:8080/blockchain/api/get_repair_history/'
        tuning_url = 'http://localhost:8080/blockchain/api/get_tuning_history/'
        replacement_url = 'http://localhost:8080/blockchain/api/get_replacement_history/'
        insurance_url = 'http://localhost:8080/blockchain/api/get_insurance_history/'
        ownership_url = 'http://localhost:8080/blockchain/api/get_ownership_history/'
        payload = {
            'registrationHash': registration_hash
        }

        repair_res = requests.post(url=repair_url, json=payload)
        tuning_res = requests.post(url=tuning_url, json=payload)
        replacement_res = requests.post(url=replacement_url, json=payload)
        insurance_res = requests.post(url=insurance_url, json=payload)
        ownership_res = requests.post(url=ownership_url, json=payload)
        if (repair_res.status_code != 200 or tuning_res.status_code != 200 or
                replacement_res.status_code != 200 or insurance_res.status_code != 200 or
                ownership_res.status_code != 200):
            raise serializers.ValidationError("blockchain error!")

        repair_data = repair_res.json()
        tuning_data = tuning_res.json()
        replacement_data = replacement_res.json()
        insurance_data = insurance_res.json()
        ownership_data = ownership_res.json()

        # 추가 데이터 넣기
        rep['repair_count'] = repair_data['count']
        rep['repair_data'] = repair_data['data']
        rep['tuning_count'] = tuning_data['count']
        rep['tuning_data'] = tuning_data['data']
        rep['replacement_count'] = replacement_data['count']
        rep['replacement_data'] = replacement_data['data']
        rep['insurance_count'] = insurance_data['count']
        rep['insurance_data'] = insurance_data['data']
        rep['ownership_count'] = ownership_data['count']
        rep['ownership_data'] = ownership_data['data']

        return rep


# 일부 정보 조회용 시리얼라이저 (일반인 - 개인정보와 보험내역을 제외 조회)
class BikePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        exclude = ['user', 'nickname', 'current_pos']
        # fields = ['model', 'manufacturer', 'is_stolen']      # 추가 예정

    # 변경 카운트 등 추가
    def to_representation(self, instance):
        # 보험/수리/튜닝/소모품 횟수 및 날짜
        # 소유자 변경 카운트/ 날짜
        rep = super().to_representation(instance)
        registration_hash = instance.registration_hash

        # 블록체인 api 호출
        repair_url = 'http://localhost:8080/blockchain/api/get_repair_history/'
        tuning_url = 'http://localhost:8080/blockchain/api/get_tuning_history/'
        replacement_url = 'http://localhost:8080/blockchain/api/get_replacement_history/'
        insurance_url = 'http://localhost:8080/blockchain/api/get_insurance_history/'
        ownership_url = 'http://localhost:8080/blockchain/api/get_ownership_history/'
        payload = {
            'registrationHash': registration_hash
        }

        repair_res = requests.post(url=repair_url, json=payload)
        tuning_res = requests.post(url=tuning_url, json=payload)
        replacement_res = requests.post(url=replacement_url, json=payload)
        insurance_res = requests.post(url=insurance_url, json=payload)
        ownership_res = requests.post(url=ownership_url, json=payload)
        if (repair_res.status_code != 200 or tuning_res.status_code != 200 or
                replacement_res.status_code != 200 or insurance_res.status_code != 200 or
                ownership_res.status_code != 200):
            raise serializers.ValidationError("blockchain error!")

        repair_data = repair_res.json()
        tuning_data = tuning_res.json()
        replacement_data = replacement_res.json()
        insurance_data = insurance_res.json()
        ownership_data = ownership_res.json()

        # 추가 데이터 넣기
        rep['repair_count'] = repair_data['count']
        rep['repair_data'] = repair_data['data']
        rep['tuning_count'] = tuning_data['count']
        rep['tuning_data'] = tuning_data['data']
        rep['replacement_count'] = replacement_data['count']
        rep['replacement_data'] = replacement_data['data']
        rep['insurance_count'] = insurance_data['count']
        rep['ownership_count'] = ownership_data['count']

        return rep


# ToDo: (완료) 블록체인 보험, 수리 내역 추가 API 작성 필요 -> blockchain app에 구현됨
# ToDo: (완료) 블록체인 소유자 이전 API 작성 필요 -> blockchain app에 구현됨


# 자전거 목록 조회 시리얼라이저
class BikeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = '__all__'


# 부품 시리얼라이저
class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'

