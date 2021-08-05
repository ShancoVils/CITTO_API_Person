from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager

OFFICIAL_LIST =(
    ("1", "Уборщик"),
    ("2", "Охранник"),
    ("3", "Кассир"),
)


class GroupPerson(models.Model):
    Name_Group = models.CharField(max_length=30, blank=True)
    

    def __str__(self):
        return self.Name_Group

class CustomUser(AbstractBaseUser, PermissionsMixin):
    fio = models.CharField(max_length=30)
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=15, blank=True )
    Official = models.CharField(max_length=1, choices=OFFICIAL_LIST)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    data_created = models.DateTimeField(default=timezone.now)
    data_update = models.DateTimeField( auto_now=True)
    date_joined = models.DateTimeField(default=timezone.now)
    token_data = models.CharField(max_length=255,blank=True)
    activate_code = models.CharField(max_length=255,blank=True)
    person_group = ForeignKey(GroupPerson, on_delete=CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

