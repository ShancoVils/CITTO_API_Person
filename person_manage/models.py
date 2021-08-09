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
    Name_Group = models.CharField(_('Название отдела'),max_length=30, blank=True)
    data_created = models.DateTimeField(_('Дата создания'),default=timezone.now)
    data_update = models.DateTimeField(_('Дата обновления'), auto_now=True)

    class Meta:
        verbose_name_plural = "Отделы"
    

    def __str__(self):
        return self.Name_Group


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('Фамилия'),max_length=30,blank=True)
    namej = models.CharField(_('Имя'),max_length=30,blank=True)
    last_name = models.CharField(_('Отчество'),max_length=30,blank=True)
    email = models.EmailField(_('Почта'), unique=True)
    official = models.CharField(_('Должность'),max_length=1, choices=OFFICIAL_LIST)
    is_staff = models.BooleanField(_('Админ'),default=False)
    is_active = models.BooleanField(_('Активирован'),default=False)
    data_created = models.DateTimeField(_('Дата создания'),default=timezone.now)
    data_update = models.DateTimeField(_('Дата обновления'), auto_now=True)
    date_joined = models.DateTimeField(default=timezone.now)
    token_data = models.CharField(_('Токен'),max_length=255,blank=True)
    activate_code = models.CharField(_('Код активации'),max_length=255,blank=True)
    person_group = ForeignKey(GroupPerson, on_delete=CASCADE, verbose_name="Отдел")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def fio(self):
        fio_field = f"{self.first_name} {self.last_name}  {self.namej}"
        return fio_field
        
    class Meta:
        verbose_name_plural = "Пользователи"



   
