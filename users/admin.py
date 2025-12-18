from django.contrib import admin
from .models import Application, Review, CustomUser

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'created_at']
    list_filter = ['status', 'created_at']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['application', 'user', 'rating', 'created_at']

admin.site.register(CustomUser)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Review, ReviewAdmin)