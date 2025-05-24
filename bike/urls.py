# bike/urls.py
from django.urls import path
from .views import RegisterView, ComponentView, BikeListView, BikeUpdateView, BikeRetrieveView

urlpatterns = [
    path('register/', RegisterView.as_view()),  # 자전거 등록 뷰
    path('update/<str:registration_hash>/', BikeUpdateView.as_view()),   # 자전거 수정 뷰
    path('<str:registration_hash>/', BikeRetrieveView.as_view()),   # 자전거 조회 뷰
    path('list/<str:username>/', BikeListView.as_view()),    # 자전거 리스트 조회 뷰
    path('component/<str:registration_hash>/', ComponentView.as_view()),     # 자전거 부품 조회&수정 뷰
]