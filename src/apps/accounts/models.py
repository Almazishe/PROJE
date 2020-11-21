from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser 
from django.contrib.auth.models import PermissionsMixin

from utils.models import BaseModel
from utils.models import DateModel

from .utils import check_user_data
from .utils import STATUS_ERROR

class AccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, password=None, **extra_fields):

        data = check_user_data(email, first_name, last_name, phone_number) # Check user data

        if data['status'] == STATUS_ERROR:
            raise ValueError(str(data['errors']))


        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password,
            **extra_fields
        )

        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff=True required for Superuser')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser=True required for Superuser')

        user.save(using=self._db)
        return user


class Account(BaseModel, DateModel, AbstractBaseUser, PermissionsMixin):
    ''' User account model '''
    VERIFIED = {
        (True, 'Verified'),
        (False, 'Not verified')
    }  

    email = models.EmailField(
        verbose_name='Email',
        max_length=64,
        unique=True,
    )  

    email_verification = models.BooleanField(
        choices=VERIFIED,
        verbose_name='Email verification:',
        default=False,
        blank=True,
    )  
    first_name = models.CharField(
        verbose_name='First name',
        max_length=100,
    )  
    last_name = models.CharField(
        verbose_name='Last name',
        max_length=100,
    )  
    phone_number = models.CharField(
        verbose_name='Phone number',
        max_length=12,
        unique=True,
    ) 

    is_staff = models.BooleanField(
        default=False,
        verbose_name='Is staff',
    )  

    is_active = models.BooleanField(
        default=True,
        verbose_name='Is active',
    )  

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'first_name', 
        'last_name', 
        'phone_number',
     )

    objects = AccountManager()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return f'{self.email} | {self.first_name} | {self.last_name}'

    def get_user_by_uuid(uuid):
        try:
            user = Account.objects.get(uuid=uuid)
            return user
        except:
            return None