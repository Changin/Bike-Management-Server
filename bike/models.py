# bike/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


# Create your models here.
# 자전거 모델
class Bike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # bike information
    manufacture_year = models.IntegerField()   # 연식
    nickname = models.CharField(max_length=8, default="자전거")      # 별명
    manufacturer = models.CharField(max_length=20)  # 제조사
    model = models.CharField(max_length=20)         # 모델명
    frame_number = models.CharField(max_length=20)    # 차대번호 (수정불가)
    weight = models.FloatField()    # 무게
    # registration information
    registration_hash = models.CharField(max_length=8, primary_key=True)  # 등록번호 (수정불가) - 블록체인 api 요청시 활용, pk
    registration_date = models.DateField()  # 등록일 (기본값 : 오늘로 설정 필요)
    purchase_date = models.DateField()      # 구매일
    # etc
    image = models.ImageField(upload_to='bike/', default='default_bike.png')    # 자전거 대표사진
    is_stolen = models.BooleanField(default=False)  # 도난 여부
    current_pos = models.TextField(blank=True)    # 도난 시 조회된 좌표

    def save(self, *args, **kwargs):
        if not self._state.adding:
            # 이미 db에 저장된 객체가 있다면 이전 값과 비교
            orig = Bike.objects.get(pk=self.pk)

            if orig.frame_number != self.frame_number:
                raise ValidationError("frame_number field 는 수정할 수 없습니다.")
            if orig.registration_hash != self.registration_hash:
                raise ValidationError("registration_hash field 는 수정할 수 없습니다.")
        super().save(*args, **kwargs)


# 부품 모델
class Component(models.Model):
    bike = models.OneToOneField(Bike, on_delete=models.CASCADE, primary_key=True)   # 자전거 모델을 1대1 필드로 연결, pk
    # Frame set
    frame = models.CharField(max_length=40, default='original')
    fork = models.CharField(max_length=40, default='original')          # 포크 & 샥(MTB)
    sitpost = models.CharField(max_length=40, default='original')
    sitclamp = models.CharField(max_length=40, default='original')
    headset = models.CharField(max_length=40, default='original')
    hanger = models.CharField(max_length=40, default='original')
    bolts = models.CharField(max_length=40, default='original')
    # Cockpit
    stem = models.CharField(max_length=40, default='original')
    handlebar = models.CharField(max_length=40, default='original')
    shiftlever = models.CharField(max_length=40, default='original')
    hood = models.CharField(max_length=40, default='original')          # 소모품 (변속 레버 후드)
    bartape = models.CharField(max_length=40, default='original')       # 소모품 (바테잎 & 그립(MTB))
    # Drivetrain (구동계)
    bb = models.CharField(max_length=40, default='original')
    crank = models.CharField(max_length=40, default='original')
    spider = models.CharField(max_length=40, default='original')
    chainring = models.CharField(max_length=40, default='original')     # 소모품 (체인링)
    sprocket = models.CharField(max_length=40, default='original')      # 소모품 (스프라켓)
    chain = models.CharField(max_length=40, default='original')         # 소모품 (체인)
    fd = models.CharField(max_length=40, default='original')
    rd = models.CharField(max_length=40, default='original')
    pulley = models.CharField(max_length=40, default='original')        # 소모품 (가이드&텐션 풀리)
    battery = models.CharField(max_length=40, default='original')
    brake = models.CharField(max_length=40, default='original')
    brakepad = models.CharField(max_length=40, default='original')      # 소모품 (브레이크 패드)
    rotor = models.CharField(max_length=40, default='original')         # 소모품 (로터(디스크브레이크))
    # Wheel
    wheelset = models.CharField(max_length=40, default='original')
    rimtape = models.CharField(max_length=40, default='original')
    qr_axle = models.CharField(max_length=40, default='original')       # QR레버 & 액슬(디스크브레이크)
    tyre = models.CharField(max_length=40, default='original')          # 소모품 (타이어)
    tube = models.CharField(max_length=40, default='original')          # 소모품 (튜브)
    # Saddle & Pedal
    saddle = models.CharField(max_length=40, default='original')
    pedal = models.CharField(max_length=40, default='original')
    # etc
    bottlecage = models.CharField(max_length=40, default='original')
    mount = models.CharField(max_length=40, default='original')     # 속도계 마운트
    sensor = models.CharField(max_length=40, default='original')
    cable = models.CharField(max_length=40, default='original')     # 소모품 (케이블 (겉선 & 속선))
    other = models.CharField(max_length=40, default='original')     # 오일, 구리스, 실란트


# Bike 모델이 post_save 이벤트를 발생시켰을 때 리스너.
# 해당 유저 인스턴스와 연결되는 Component 데이터를 생성
@receiver(post_save, sender=Bike)
def create_bike_component(sender, instance, created, **kwargs):
    if created:
        Component.objects.create(bike=instance)