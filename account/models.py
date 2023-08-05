from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _



# Customizing User Model
class UserManager(BaseUserManager):
    use_in_migrations = True
    # base
    def _create_user(self, username, email, password, **extra_fields):
        if not username: 
            raise ValueError('Users must have a name')
        if not email:
            raise ValueError('Users must have an email address')
        username = self.model.normalize_username(username)
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    # normal user
    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)
    
    # super user
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must be "is_superuser=True".')
        return self._create_user(username, email, password, **extra_fields)

    
class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(_('username'), max_length=30, validators=[username_validator])
    email = models.EmailField(_('email_address'), max_length=255, unique=True)
    is_superuser = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email' # 로그인이나 메일 송신등에 이용
    EMAIL_FIELD = ['email', 'username'] # 유저생성에 표시되는 항목
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
