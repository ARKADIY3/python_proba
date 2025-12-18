# admin.py - НАСТРАИВАЕМ отображение заявок
from django.contrib import admin
from .models import Application, Review, CustomUser


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    # Какие поля показывать в списке
    list_display = ['title', 'user', 'status', 'created_at', 'payment_method']

    # Фильтры справа
    list_filter = ['status', 'payment_method', 'created_at']

    # Поиск по полям
    search_fields = ['title', 'user__username', 'user__email']

    # Порядок сортировки (новые сверху)
    ordering = ['-created_at']

    # Поля только для чтения при редактировании
    readonly_fields = ['created_at']


# Остальные модели как были
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['application', 'user', 'rating', 'created_at']


admin.site.register(CustomUser)