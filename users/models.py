from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a new user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a new superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    def authenticate_user(self, email, password):
        """
        Authenticates user with the given email and password.
        """
        user = authenticate(username=email, password=password)
        return user

    def create_and_authenticate_user(self, username, email, password):
        """
        Creates and authenticates user with the given email, username and password.
        """
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('Invalid email format')

        if self.filter(email=email).exists():
            raise ValueError('This email already in use.')

        user = self.create_user(email=email, username=username, password=password)
        user = self.authenticate_user(email=email, password=password)
        return user
    
    def is_user_account_verified(self, user):
        return user.is_verified if user else False
    
    def does_user_exist(self, email):
        """
        Returns True if a user account with the given email exists.
        """
        return self.filter(email=email).exists()
    
    def get_user_by_email(self, email):
        """
        Returns a user object for the given email.
        """
        try:
            return self.get(email=email)
        except self.model.DoesNotExist:
            return None

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email address'), unique=True)
    username =  models.CharField(_('Username'), max_length=30, blank=True)
    first_name = models.CharField(_('First name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last name'), max_length=30, blank=True)
    is_verified = models.BooleanField(_('Is verified'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)
    is_staff = models.BooleanField(_('Staff'), default=False)
    is_autoleads_creator = models.BooleanField(_('Autoleads creator'), default=False)
    profile_picture_url = models.URLField(_('Profile picture URL'), blank=True)
    date_joined = models.DateTimeField(_('Date joined'), auto_now_add=True)
    provider = models.CharField(_('Account provider'), max_length=30, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        app_label = 'users'

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Returns the first name and last name of the user.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission.
        """
        return self.is_staff

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        """
        return self.is_staff
