# Generated by Django 3.2.9 on 2021-12-06 11:36

from django.db import migrations, models
import instagram.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=60, unique=True, verbose_name='Username аккаунта')),
                ('password', models.CharField(max_length=60, verbose_name='Пароль аккаунта')),
                ('active', models.BooleanField(default=True, verbose_name='Указывает, необходимо ли брать аккаунт для логина')),
                ('worked', models.BooleanField(default=True, verbose_name='Указывает успешность последнего логина')),
                ('last_attempt', models.DateTimeField(blank=True, null=True, verbose_name='Время последней попытки логина')),
                ('last_active', models.DateTimeField(blank=True, null=True, verbose_name='Время последнего успешного логина аккаунта')),
                ('error_codes', models.JSONField(default={}, verbose_name='Коды ошибок')),
                ('cookie', models.FileField(blank=True, null=True, upload_to=instagram.models.path_to_cookies, verbose_name='Куки для входа аккаунта')),
            ],
            options={
                'verbose_name': 'Инстаграм аккаунт',
                'verbose_name_plural': 'Инстаграм аккаунты',
            },
        ),
        migrations.CreateModel(
            name='UserObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='Ник наблюдаемого пользователя')),
                ('activate', models.BooleanField(blank=True, default=True, verbose_name='Параметр, отвечающие за необходимость обновления данных о пользователе')),
                ('id_insta', models.PositiveBigIntegerField(blank=True, default=0, verbose_name='id пользователя в Instagram')),
                ('full_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Полное имя пользователя в Instagram')),
                ('is_private', models.BooleanField(default=False, verbose_name='Приватный ли аккаунт')),
                ('media_count', models.PositiveIntegerField(blank=True, default=0, verbose_name='Количество записей пользователя')),
                ('follower_count', models.PositiveIntegerField(blank=True, default=0, verbose_name='Количество подписчиков пользователя')),
                ('following_count', models.PositiveIntegerField(blank=True, default=0, verbose_name='Количество пользователей на которых подписан объект наблюдения')),
                ('biography', models.CharField(blank=True, max_length=1500, null=True, verbose_name='Биография пользователя')),
                ('external_link', models.CharField(blank=True, max_length=250, null=True, verbose_name='Внешние ссылки пользователя')),
                ('email', models.CharField(blank=True, max_length=150, null=True, verbose_name='Email пользователя')),
                ('phone', models.CharField(blank=True, max_length=30, null=True, verbose_name='Телефон пользователя')),
                ('is_business', models.BooleanField(blank=True, default=False, verbose_name='Является ли аккаунт бизнес аккаунтом')),
                ('business_category', models.CharField(blank=True, max_length=200, null=True, verbose_name='Категория бизнес аккаунта')),
                ('instagram_link', models.CharField(blank=True, max_length=250, null=True, verbose_name='Ссылка на аккаунт Instagram')),
                ('last_update', models.DateTimeField(auto_now_add=True, verbose_name='Показывает время последнего обновление данных пользователя')),
                ('is_updated', models.BooleanField(blank=True, default=True, verbose_name='Указывает, находится ли данные об аккаунте в процессе обновления')),
                ('pic', models.ImageField(blank=True, null=True, upload_to='icon/', verbose_name='Хранит иконку профиля пользователя')),
                ('medias', models.JSONField(blank=True, default={}, verbose_name='Хранит информацию об ресурсах с главной страницы')),
                ('stories', models.JSONField(blank=True, default={}, verbose_name='Хранит информацию о ресурсах с историй')),
            ],
            options={
                'verbose_name': 'Наблюдаемый аккаунт',
                'verbose_name_plural': 'Наблюдаемые аккаунты',
            },
        ),
    ]
