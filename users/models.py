# users/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # primary_key를 User의 pk로 설정해 통합 관리
    birthday = models.CharField(max_length=6)   # 주민번호 앞자리
    phone = models.CharField(max_length=15)     # 연락처
    image = models.ImageField(upload_to='profile/', default='default.png')  # 프로필사진 경로


# User 모델이 post_save 이벤트를 발생시켰을 때 리스너.
# 해당 유저 인스턴스와 연결되는 Profile 데이터를 생성
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)