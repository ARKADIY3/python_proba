from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import RegisterForm, ReviewForm, ApplicationForm
from .models import Application, Review


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Редирект после успеха
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        # Создаем форму авторизации с данными из запроса
        form = AuthenticationForm(data=request.POST)

        # Проверяем валидность формы
        if form.is_valid():
            # Получаем пользователя из формы
            user = form.get_user()

            # Выполняем вход пользователя
            login(request, user)

            # Перенаправляем на главную страницу
            return redirect('home')
    else:
        # Если GET запрос - создаем пустую форму
        form = AuthenticationForm()

    # Отображаем форму авторизации
    return render(request, 'login.html', {'form': form})


# Функция выхода
def logout_view(request):
    logout(request)
    return redirect('login')
def home_view(request):
    return render(request, 'home.html', {'user': request.user})


@login_required
def applications_view(request):
    # Получаем все заявки текущего пользователя
    user_applications = Application.objects.filter(user=request.user)

    # Если форма отправлена
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Получаем ID заявки из скрытого поля
            application_id = request.POST.get('application_id')
            application = Application.objects.get(id=application_id, user=request.user)

            # Создаем отзыв
            review = form.save(commit=False)
            review.application = application
            review.user = request.user
            review.save()

            return redirect('applications')

    # Для GET запроса создаем пустую форму
    form = ReviewForm()

    # Собираем данные о заявках и отзывах
    applications_data = []
    for app in user_applications:
        try:
            review = Review.objects.get(application=app)
            has_review = True
        except Review.DoesNotExist:
            review = None
            has_review = False

        applications_data.append({
            'application': app,
            'has_review': has_review,
            'review': review
        })

    return render(request, 'applications.html', {
        'applications_data': applications_data,
        'form': form
    })


from django.contrib.auth.decorators import login_required


@login_required
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            return redirect('applications')
    else:
        form = ApplicationForm()

    return render(request, 'create_application.html', {'form': form})