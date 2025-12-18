from django.contrib import admin
from .models import Application, Review, CustomUser


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'created_at', 'payment_method']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['title', 'user__username', 'user__email']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['application', 'user', 'rating', 'created_at']


admin.site.register(CustomUser)