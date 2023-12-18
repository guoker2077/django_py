from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


# Create your models here.
class UserInfo(models.Model):
    # 用户名关联
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='/media/11.png')
    # 手机号限制：必须是11位数字
    phone_regex = RegexValidator(regex=r'^\d{11}$', message="手机号必须是11位数字")
    phone = models.CharField(validators=[phone_regex], max_length=11, blank=False)

    # 姓名可以为空
    name = models.CharField(max_length=100, null=True, blank=True)

    # 性别选项
    GENDER_CHOICES = (
        ('男', '男'),
        ('女', '女'),
        ('不便透露', '不便透露'),
        ('跨性别认知者', '跨性别认知者'),
    )
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
        default='不便透露'  # 设置默认性别为"不便透露"
    )

    # 年龄限制：正整数且不超过120
    age = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        default=0  # 设置默认年龄为0
    )

    # 账户余额限制：非负数，初始值为0.00
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00)]
    )

    def __str__(self):
        return self.user.username
