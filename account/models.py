from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _



# Customizing User Model
class MyUserManager(BaseUserManager):
    use_in_migrations = True
    # base
    def _create_user(self, name, email, password, **extra_fields):
        if not name: 
            raise ValueError('Users must have a name')
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            name=name, 
            email=self.normalize_email(email), 
            **extra_fields,
            )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    # normal user
    def create_user(self, name, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)
    
    # super user
    def create_superuser(self, name, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('staff must be True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must be True.')
        return self._create_user(name, email, password, **extra_fields)

    
class MyUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(_('name'), max_length=30)
    email = models.EmailField(_('email_address'), max_length=255, unique=True)
    is_staff = models.BooleanField(_('is staff'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = MyUserManager()

    USERNAME_FIELD = 'email' # 로그인이나 메일 송신등에 이용
    REQUIRED_FIELDS = ['name']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')