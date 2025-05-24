# users/urls.py
from django.urls import path
from .views import RegisterView, LoginView, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view()),  # 회원가입 뷰
    path('login/', LoginView.as_view()),    # 로그인 뷰
    path('profile/<int:pk>/', ProfileView.as_view()),   # 프로필 뷰
]