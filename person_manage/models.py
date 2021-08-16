from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from requests.api import delete
from .managers import CustomUserManager
import datetime
OFFICIAL_LIST =(
    ("1", "Уборщик"),
    ("2", "Охранник"),
    ("3", "Кассир"),
    ("4", "Разработчик"),
    ("5", "Оператор"),
    ("6", "Директор"),

)


'''

Класс создает модель "Отделы". В каждом отделе может быть сколько угодно пользователей

'''
class GroupPerson(models.Model):
    Name_Group = models.CharField(_('Название отдела'),max_length=30, blank=True)
    max_test_factor = models.FloatField(_('Максимальный коэффициент'),max_length=10, blank=True)
    pass_test_factor = models.FloatField(_('Проходной коэффициент'),max_length=10, blank=True)
    data_created = models.DateTimeField(_('Дата создания'),default=timezone.now)
    data_update = models.DateTimeField(_('Дата обновления'), auto_now=True)

    class Meta:
        verbose_name_plural = "Отделы"
    
    def __str__(self):
        return self.Name_Group

'''

Класс создает модель "Пользователь"

'''       
class CustomUser(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()
    first_name = models.CharField(_('Фамилия'),max_length=30,blank=True)
    namej = models.CharField(_('Имя'),max_length=30,blank=True)
    last_name = models.CharField(_('Отчество'),max_length=30,blank=True)
    email = models.EmailField(_('Почта'), unique=True)
    official = models.CharField(_('Должность'),max_length=1, choices=OFFICIAL_LIST, default=1)
    is_staff = models.BooleanField(_('Админ'),default=False)
    is_active = models.BooleanField(_('Активирован'),default=False)
    data_created = models.DateTimeField(_('Дата создания'),default=timezone.now)
    data_update = models.DateTimeField(_('Дата обновления'), auto_now=True)
    date_joined = models.DateTimeField(default=timezone.now)
    token_data = models.CharField(_('Токен'),max_length=255,blank=True)
    activate_code = models.CharField(_('Код активации'),max_length=255,blank=True)
    person_group = ForeignKey(GroupPerson, on_delete=CASCADE, verbose_name="Отдел")
    fio = models.CharField(_('ФИО'),max_length=255, blank=True)

    def save(self):
        if not self.fio:
           self.fio = f"{self.first_name} {self.last_name}  {self.namej}"
        return super(CustomUser, self).save()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name_plural = "Пользователи"

'''

Класс создает модель "Вопросы". Вопосы заносятся в бд вручную

'''
class QuestionsPull(models.Model):
    question = models.CharField(_('Вопрос'),max_length=255)
    answer = models.CharField(_('Ответ'),max_length=30,)
    data_created = models.DateTimeField(_('Дата создания'),default=timezone.now)
    data_update = models.DateTimeField(_('Дата обновления'), auto_now=True)
    factor = models.FloatField(_('Коэффициент'),)
    class Meta:
            verbose_name_plural = "Вопросы"

'''

 Класс создает модель "Тестирование". Вопосы заносятся в бд автоматически.

 '''
class TestResults(models.Model):
    tested_user = models.ForeignKey(CustomUser, on_delete=CASCADE, verbose_name="Пользователь")
    test_questions = models.JSONField(_('Вопросы'),max_length=255)
    test_answers = models.JSONField(_('Ответы'),max_length=255,null=True, blank=True)
    test_sum_factor = models.IntegerField(_('Результат'),null=True, blank=True)
    test_result = models.CharField(_('Итог'),max_length=255,null=True, blank=True)
    test_time_begin = models.TimeField(_('Время начала теста'),null=True, blank=True)
    test_time_end = models.TimeField(_('Время конца теста'),null=True, blank=True)


    class Meta:
        verbose_name_plural = "Тестирование"


