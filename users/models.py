from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


class CustomUser(AbstractUser):
    full_name = models.CharField(
        max_length=100,
        validators=[RegexValidator(r'^[А-Яа-яЁё\s]+$', 'Только кириллица и пробелы')]
    )
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$', 'Формат: 8(XXX)XXX-XX-XX')]
    )
    email = models.EmailField(unique=True)

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(r'^[a-zA-Z0-9]{6,}$', 'Латиница и цифры, минимум 6 символов')]
    )


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('approved', 'Одобрено'),
        ('completed', 'Завершено'),
        ('rejected', 'Отклонено'),
    ]

    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField('Название заявки', max_length=200)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

class Review(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, verbose_name='Заявка')
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.IntegerField('Оценка', validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f"Отзыв на {self.application.title} - {self.rating}/5"