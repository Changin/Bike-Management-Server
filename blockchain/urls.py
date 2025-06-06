from django.urls import path
from . import views

urlpatterns = [
    # 🔹 자전거 등록
    path('api/register_bicycle/', views.register_bicycle, name='register_bicycle'),
    path('api/get_registration_hash/', views.get_registration_hash, name='get_registration_hash'),

    # 🔹 이력 추가
    path('api/add_tuning_history/', views.add_tuning_history, name='add_tuning_history'),
    path('api/add_replacement_history/', views.add_replacement_history, name='add_replacement_history'),
    path('api/add_repair_history/', views.add_repair_history, name='add_repair_history'),
    path('api/add_insurance_history/', views.add_insurance_history, name='add_insurance_history'),

    # 🔹 소유권 이전 & 도난 신고
    path('api/transfer_ownership/', views.transfer_ownership, name='transfer_ownership'),
    path('api/report_stolen/', views.report_stolen, name='report_stolen'),

    # 🔹 조회 API
    path('api/get_bicycle_info/', views.get_bicycle_info, name='get_bicycle_info'),
    path('api/get_all_bicycles/', views.get_all_bicycles, name='get_all_bicycles'),

    # 🔹 이력 구조체 조회 (각 이력별로 따로 요청)
    path('api/get_tuning_history/', views.get_tuning_history, name='get_tuning_history'),
    path('api/get_replacement_history/', views.get_replacement_history, name='get_replacement_history'),
    path('api/get_repair_history/', views.get_repair_history, name='get_repair_history'),
    path('api/get_insurance_history/', views.get_insurance_history, name='get_insurance_history'),
    path('api/get_ownership_history/', views.get_ownership_history, name='get_ownership_history'),

    #  기능 등록된 전체 차대번호 조회
    path('api/get_all_bicycles/', views.get_all_bicycles, name='get_all_bicycles'),

    # qr생성
     path('api/generate_qr/', views.generate_qr,name='generate_qr'),
]