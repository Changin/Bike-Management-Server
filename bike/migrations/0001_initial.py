# Generated by Django 5.2.1 on 2025-05-22 08:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Bike",
            fields=[
                ("manufacture_year", models.IntegerField()),
                ("nickname", models.CharField(max_length=8)),
                ("manufacturer", models.CharField(max_length=20)),
                ("model", models.CharField(max_length=20)),
                ("frame_number", models.CharField(max_length=20)),
                ("weight", models.FloatField()),
                (
                    "registration_hash",
                    models.CharField(max_length=8, primary_key=True, serialize=False),
                ),
                ("registration_date", models.DateField()),
                ("purchase_date", models.DateField()),
                (
                    "image",
                    models.ImageField(default="default_bike.png", upload_to="bike/"),
                ),
                ("is_stolen", models.BooleanField(default=False)),
                ("current_pos", models.TextField(default="")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Component",
            fields=[
                (
                    "bike",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="bike.bike",
                    ),
                ),
                ("frame", models.CharField(default="original", max_length=40)),
                ("fork", models.CharField(default="original", max_length=40)),
                ("sitpost", models.CharField(default="original", max_length=40)),
                ("sitclamp", models.CharField(default="original", max_length=40)),
                ("headset", models.CharField(default="original", max_length=40)),
                ("hanger", models.CharField(default="original", max_length=40)),
                ("bolts", models.CharField(default="original", max_length=40)),
                ("stem", models.CharField(default="original", max_length=40)),
                ("handlebar", models.CharField(default="original", max_length=40)),
                ("shiftlever", models.CharField(default="original", max_length=40)),
                ("hood", models.CharField(default="original", max_length=40)),
                ("bartape", models.CharField(default="original", max_length=40)),
                ("bb", models.CharField(default="original", max_length=40)),
                ("crank", models.CharField(default="original", max_length=40)),
                ("spider", models.CharField(default="original", max_length=40)),
                ("chainring", models.CharField(default="original", max_length=40)),
                ("sprocket", models.CharField(default="original", max_length=40)),
                ("chain", models.CharField(default="original", max_length=40)),
                ("fd", models.CharField(default="original", max_length=40)),
                ("rd", models.CharField(default="original", max_length=40)),
                ("pulley", models.CharField(default="original", max_length=40)),
                ("battery", models.CharField(default="original", max_length=40)),
                ("brake", models.CharField(default="original", max_length=40)),
                ("brakepad", models.CharField(default="original", max_length=40)),
                ("rotor", models.CharField(default="original", max_length=40)),
                ("wheelset", models.CharField(default="original", max_length=40)),
                ("rimtape", models.CharField(default="original", max_length=40)),
                ("qr_axle", models.CharField(default="original", max_length=40)),
                ("tyre", models.CharField(default="original", max_length=40)),
                ("tube", models.CharField(default="original", max_length=40)),
                ("saddle", models.CharField(default="original", max_length=40)),
                ("pedal", models.CharField(default="original", max_length=40)),
                ("bottlecage", models.CharField(default="original", max_length=40)),
                ("mount", models.CharField(default="original", max_length=40)),
                ("sensor", models.CharField(default="original", max_length=40)),
                ("cable", models.CharField(default="original", max_length=40)),
                ("other", models.CharField(default="original", max_length=40)),
            ],
        ),
    ]
