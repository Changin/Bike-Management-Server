# users/views.py

from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from .models import Profile
from .permissions import CustomReadOnly


# Create your views here.
# REST API 뷰 사용, 클래스형 뷰
# 회원 생성 기능 한개만 있기 떄문에 굳이 ViewSet 필요없음.
# CreateAPIView : POST 만 지원 - 객체 생성 가능
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# 로그인 뷰
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data   # validate()의 반환값 token을 받아온다
        return Response({"token": token.key}, status=status.HTTP_200_OK)


# 프로필 불러오기와 수정 기능이 구현된 APIView 사용
# RetrieveUpdateAPIView : GET, PUT, PATCH - 조회 + 수정만 가능
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [CustomReadOnly]   # 특정 권한이 필요할 때 이 필드 설정해서 구현 가능
