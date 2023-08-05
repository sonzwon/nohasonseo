from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from account.models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )

    username = forms.CharField(max_length=30, help_text='이름을 입력하세요', label='이름')
    email = forms.EmailField(max_length=255, help_text='이메일을 입력하세요', label='이메일')


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'이메일'})
        )
    password = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'비밀번호'})
        )
    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class':'custom-control-input', 'id':'_loginRemeberMe'}),
        required=False,
        disabled=False
        )