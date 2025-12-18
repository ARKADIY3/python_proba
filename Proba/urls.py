from django.urls import path
from users import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),  # Обновляем - см. ниже
    path('applications/', views.applications_view, name='applications'),
]