from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator

from .models import CustomUser, Review


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин',)
    full_name = forms.CharField(label='ФИО')
    phone = forms.CharField(label='Телефон')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(
        label='Пороль',
        widget=forms.PasswordInput,
        validators=[MinLengthValidator(8, 'Минимум 8 символов')]
    )
    password2 = forms.CharField(label='Подтверждение пороля',)

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'phone', 'email', 'password1', 'password2']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {
            'rating': 'Оценка (от 1 до 5)',
            'comment': 'Комментарий'
        }
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 3})
        }