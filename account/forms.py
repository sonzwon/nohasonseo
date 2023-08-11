
from django import forms
from account.models import MyUser
from argon2 import PasswordHasher, exceptions
from django.contrib.auth import login


class SignUpForm(forms.ModelForm):
    name = forms.CharField(
        max_length=30, 
        label='사용자 이름',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'사용자 이름'
            }),
        error_messages={'required':'이름을 입력해주세요'})
    email = forms.EmailField(
        max_length=255, 
        label='이메일',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class':'form-control',
                'placeholder':'이메일'
            }),
        error_messages={'required':'이메일을 입력해주세요'})
    password1 = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'placeholder':'비밀번호'
            }),
            )
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'placeholder':'비밀번호 확인'
            }),)

    class Meta:
        model = MyUser
        fields = (
            'name',
            'email',
            'password1',
            'password2',
        )
    
    def clean(self):
        cleaned_data = super().clean()

        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            return self.add_error("Passwords don't match")
        else:
            self.name = name
            self.email = email
            self.password1 = PasswordHasher().hash(password1)
            self.password2 = password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user




class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={'class':'form-control', 
                   'placeholder':'이메일'})
        )
    password = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 
                   'placeholder':'비밀번호'})
        )
    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class':'custom-control-input', 
                   'id':'_loginRemeberMe'}),
        required=False,
        disabled=False
        )
    
    field_order = ['email', 'password']

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        try:
            user = MyUser.objects.get(email=email)
            if user.name == 'admin' and user.check_password(password):
                return user
        except:
            return self.add_error('email', '사용자를 찾을 수 없습니다')

        try:
            PasswordHasher().verify(user.password, password)
        except exceptions.VerifyMismatchError:
            return self.add_error('password', '비밀번호가 다릅니다')