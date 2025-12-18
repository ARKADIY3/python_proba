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


# models.py - МЕНЯЕМ статусы
class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),  # ← Изначальный статус
        ('in_progress', 'Идет обучение'),  # ← Админ может сменить
        ('completed', 'Обучение завершено'),  # ← Финальный статус
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод по номеру телефона'),
    ]

    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField('Наименование курса', max_length=200)
    start_date = models.DateField('Дата начала обучения', default='2025-01-01')
    payment_method = models.CharField('Способ оплаты', max_length=20, choices=PAYMENT_CHOICES, default='cash')
    description = models.TextField('Дополнительные пожелания', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')  # ← default='new'

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