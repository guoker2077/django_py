from django import forms
from .models import UserInfo


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    phone = forms.CharField(label='手机号', max_length=11)
    # 其他字段...


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['avatar', 'name', 'phone', 'gender', 'balance', 'age']
        # 其他字段...
