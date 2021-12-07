import os

from django.db import models

from configs import settings
from utils.time import edit_current_time


class UserObject(models.Model):
    """
    Модель наблюдаемого пользователя

    username: string;
    activate: bool;
    id_insta: integer;
    full_name: string;
    is_private: bool;
    media_count: int;
    follower_count: int;
    following_count: int;
    biography: string;
    external_link: string;
    email: string;
    phone: string;
    is_business: bool;
    business_category: string;
    instagram_link: string;
    last_update: datetime;
    is_updated: bool;
    pic: ImageField;


    medias: {
        id (int): {  - где id идентификатор ресурса в Instagram
            type: Union['photo', 'feed', 'igtv, 'clips', 'album']; - тип ресурса
            likes: int; - количество лайков
            comments: int; - количество комментариев
            date: datetime; - дата опубликования
            link: - ссылка на ресурс
            objects: [  - массив с объектами ресурса
                {
                  name: str;  - наименование объекта
                  count: int;   - количество таких объектов ресурса
                },
            ];
            hashtags: [name_hashtag: str]; - хештеги ресурса
            friends: [username: str]; - отмеченные пользователя ресурса
        }
    }

    stories: {
        id (int): {  - где id идентификатор ресурса в Instagram
            type: Union['photo', 'feed', 'igtv, 'clips']; - тип ресурса
            date: datetime; - дата опубликования
            objects: [  - массив с объектами ресурса
                {
                  name: str;  - наименование объекта
                  count: int;   - количество таких объектов ресурса
                },
            ];
            hashtags: [name_hashtag: str]; - хештеги ресурса
            friends: [username: str]; - отмеченные пользователя ресурса
        }
    }
    """

    username = models.CharField(
        unique=True,
        max_length=50,
        verbose_name='Ник наблюдаемого пользователя'
    )

    activate = models.BooleanField(
        default=True,
        verbose_name='Параметр, отвечающие за необходимость обновления данных о пользователе',
        blank=True
    )

    id_insta = models.PositiveBigIntegerField(
        default=0,
        verbose_name="id пользователя в Instagram",
        blank=True
    )

    full_name = models.CharField(
        verbose_name="Полное имя пользователя в Instagram",
        max_length=250,
        blank=True,
        null=True
    )

    is_private = models.BooleanField(
        default=False,
        verbose_name="Приватный ли аккаунт"
    )

    media_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество записей пользователя",
        blank=True
    )

    follower_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество подписчиков пользователя",
        blank=True
    )

    following_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество пользователей на которых подписан объект наблюдения",
        blank=True
    )

    biography = models.CharField(
        max_length=1500,
        verbose_name="Биография пользователя",
        blank=True,
        null=True
    )

    external_link = models.CharField(
        max_length=250,
        verbose_name="Внешние ссылки пользователя",
        blank=True,
        null=True
    )

    email = models.CharField(
        max_length=150,
        verbose_name="Email пользователя",
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=30,
        verbose_name="Телефон пользователя",
        blank=True,
        null=True
    )

    is_business = models.BooleanField(
        default=False,
        verbose_name="Является ли аккаунт бизнес аккаунтом",
        blank=True
    )

    business_category = models.CharField(
        max_length=200,
        verbose_name="Категория бизнес аккаунта",
        blank=True,
        null=True
    )

    instagram_link = models.CharField(
        max_length=250,
        verbose_name="Ссылка на аккаунт Instagram",
        blank=True,
        null=True
    )

    last_update = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Показывает время последнего обновление данных пользователя"
    )

    is_updated = models.BooleanField(
        default=True,
        verbose_name="Указывает, находится ли данные об аккаунте в процессе обновления",
        blank=True
    )

    pic = models.ImageField(
        upload_to="icon/",
        null=True,
        verbose_name="Хранит иконку профиля пользователя",
        blank=True
    )

    medias = models.JSONField(
        blank=True,
        default=dict(),
        verbose_name='Хранит информацию об ресурсах с главной страницы'
    )
    stories = models.JSONField(
        blank=True,
        default=dict(),
        verbose_name='Хранит информацию о ресурсах с историй'
    )

    def __str__(self):
        return self.username

    def delete(self, using=None, keep_parents=False):
        if self.pic:
            self.pic.storage.delete(self.pic.name)
        super().delete()

    class Meta:
        verbose_name = 'Наблюдаемый аккаунт'
        verbose_name_plural = 'Наблюдаемые аккаунты'


def path_to_cookies(instance, filename: str = 'useless') -> str:
    return f'cookies/{instance.username}.json'


class InstagramLogin(models.Model):
    """
    Модель для хранения аккаунтов инстаграм, предназначенных для
    логина в инстаграм с целью проверки заданий
    """

    username = models.CharField(max_length=60, unique=True, verbose_name='Username аккаунта')
    password = models.CharField(max_length=60, verbose_name='Пароль аккаунта')

    active = models.BooleanField(default=True, verbose_name='Указывает, необходимо ли брать аккаунт для логина')

    worked = models.BooleanField(default=True, verbose_name='Указывает успешность последнего логина')
    last_attempt = models.DateTimeField(null=True, blank=True, verbose_name='Время последней попытки логина')
    last_active = models.DateTimeField(null=True, blank=True, verbose_name='Время последнего успешного логина аккаунта')

    # key - datetime, value - error_code
    error_codes = models.JSONField(default=dict(), verbose_name='Коды ошибок')

    cookie = models.FileField(null=True, blank=True, upload_to=path_to_cookies, verbose_name='Куки для входа аккаунта')

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        """
        Переопределяю save для того, чтобы FileField
        присваивались куки файлы аккаунта, если они есть
        """
        super(InstagramLogin, self).save(*args, **kwargs)
        if not self.cookie:
            path_to_cookie = os.path.join(settings.BASE_DIR, 'media/' + path_to_cookies(self))
            if os.path.exists(path_to_cookie):
                self.cookie.name = path_to_cookie
                self.save()

    def add_error(self, string) -> None:
        """
        Добавляет ошибку в error_codes
        """
        self.error_codes[str(edit_current_time())] = string
        self.save()

    def successful_login(self) -> None:
        """
        Вносит пометки, если был произведен успешный логин
        """
        time = edit_current_time()
        self.worked = True
        self.last_active = time
        self.last_attempt = time
        self.save()

    def unsuccessful_login(self, exception: str) -> None:
        """
        Вносит пометки, если был произведен неуспешный логин
        """
        time = edit_current_time()
        self.error_codes[str(time)] = exception
        self.worked = False
        self.last_attempt = time
        self.save()

    class Meta:
        verbose_name = 'Инстаграм аккаунт'
        verbose_name_plural = 'Инстаграм аккаунты'