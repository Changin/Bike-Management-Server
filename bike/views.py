# bike/views.py
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import (RegisterSerializer, ComponentSerializer, BikeListSerializer, BikeUpdateSerializer,
                          BikeDetailSerializer, BikePublicSerializer)
from .models import Component, Bike
from .permissions import CustomReadOnly, CustomBikeReadOnly

import requests


# Create your views here.
# REST API 뷰 사용, 클래스형 뷰, 자전거 생성 기능
# CreateAPIView : POST 만 지원 - 객체 생성 가능
class RegisterView(generics.CreateAPIView):
    queryset = Bike.objects.all()
    serializer_class = RegisterSerializer


# 자전거 정보 수정 기능
# RetrieveUpdateAPIView : GET, PATCH 지원
class BikeUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeUpdateSerializer
    permission_classes = [CustomBikeReadOnly]

    lookup_field = 'registration_hash'     # url에서 이 필드로 조회


# 자전거 조회 기능
# RetrieveAPIView : GET 지원
# 권한별로 정보조회 범위 다르게 설정
class BikeRetrieveView(generics.RetrieveAPIView):
    queryset = Bike.objects.all()
    lookup_field = 'registration_hash'
    permission_classes = []     # 누구나 접근 가능 (비인증자)

    def get_serializer_class(self):
        bike = self.get_object()
        user = self.request.user

        if user.is_authenticated and bike.user == user:
            # 소유자 본인
            return BikeDetailSerializer
        return BikePublicSerializer  # 본인이 아닌 경우 제한 정보


# 자전거 리스트 조회 기능
# ListAPIView : GET 만 지원 - 리스트 반환
class BikeListView(generics.ListAPIView):
    serializer_class = BikeListSerializer

    def get_queryset(self):
        username = self.kwargs.get('username')
        return Bike.objects.filter(user__username=username)


# 부품 불러오기와 수정 기능이 구현된 RetrieveUpdateAPIView 사용
# registration_hash 기반으로 조회
# RetrieveUpdateAPIView : GET, PUT, PATCH - 조회 + 수정만 가능
class ComponentView(generics.RetrieveUpdateAPIView):
    serializer_class = ComponentSerializer
    permission_classes = [CustomReadOnly]   # 특정 권한이 필요할 때 이 필드 설정해서 구현 가능 (get은 누구나, 수정은 본인만 가능)

    def get_object(self):
        registration_hash = self.kwargs.get('registration_hash')
        bike = get_object_or_404(Bike, registration_hash=registration_hash)
        component = get_object_or_404(Component, bike=bike)
        self.check_object_permissions(self.request, component)
        return component

    def update(self, request, *args, **kwargs):
        # 소모품 교체, 튜닝 : 부품 내역 수정이 발생할 경우 블록체인 API 호출
        partial = kwargs.pop('partial', False)  # PATCH일 경우 partial=True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if request.method == 'PATCH':
            # ----------------- 여기서 Web3 로직 수행 ------------- #
            expendables = ('hood', 'bartape', 'chainring', 'sprocket', 'chain',
                           'pulley', 'brakepad', 'rotor', 'tyre', 'tube', 'cable', 'other')

            for key, value in request.data.items():
                if key in expendables:
                    # 소모품의 경우 교체이력 추가 api 호출
                    url = 'http://localhost:8080/blockchain/api/add_replacement_history/'
                    payload = {
                        'registrationHash': self.kwargs.get('registration_hash'),
                        'replacementCID': key + ':' + value
                    }
                    response = requests.post(url=url, json=payload)
                    if response.status_code != 200:
                        print('blockchain patch error!')
                        return Response({'error': 'blockchain patch error!'}, status=500)
                else:
                    # 튜닝의 경우 튜닝이력 추가 api 호출
                    url = 'http://localhost:8080/blockchain/api/add_tuning_history/'
                    payload = {
                        'registrationHash': self.kwargs.get('registration_hash'),
                        'tuningCID': key + ':' + value
                    }
                    response = requests.post(url=url, json=payload)
                    if response.status_code != 200:
                        print('blockchain tuning error! '+ response.status_code)
                        return Response({'error': 'tuning blockchain error'}, status=500)

        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
