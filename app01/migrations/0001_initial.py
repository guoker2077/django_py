# Generated by Django 4.2.7 on 2023-11-28 12:45

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        max_length=11,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="手机号必须是11位数字", regex="^\\d{11}$"
                            )
                        ],
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("男", "男"),
                            ("女", "女"),
                            ("不便透露", "不便透露"),
                            ("跨性别认知者", "跨性别认知者"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "age",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(120),
                        ],
                    ),
                ),
                (
                    "balance",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]