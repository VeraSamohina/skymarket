from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models
from .managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField


class UserRoles(models.TextChoices):
    USER = 'user'
    ADMIN = 'admin'


class User(AbstractBaseUser):
    """
        Определяем модель пользователя.
        Добавляем авторизацию по email и расширяем модель дополнительной информацией:
        номер телефона, аватар, chat_id (для уведомлений в телеграмм)

        Attributes:
            first_name (str): Имя.
            last_name (str)): Фамилия.
            phone (PhoneNumberField: Номер телефона пользователя.
            image(ImageField): Аватар
            role (str): Роль - администратор или пользователь
        """

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone = PhoneNumberField(max_length=35, blank=True, verbose_name='Телефон')
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='users/', null=True, blank=True, verbose_name='Аватар')
    role = models.CharField(max_length=50, choices=UserRoles.choices, default=UserRoles.USER, verbose_name='Роль')
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', "role"]

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
