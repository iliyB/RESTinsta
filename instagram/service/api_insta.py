import datetime
from typing import Optional

import requests
from django.core.files.base import ContentFile
from instagrapi import Client
from instagrapi.exceptions import RateLimitError

from configs import settings
from instagram.models import InstagramLogin, path_to_cookies, UserObject
from instagram.service.database import set_info_about_user, is_updated_set_true, update_time
from instagram.utils import get_account


def change_instagram_client():
    """
    Меняет аккаунт для входа в инстаграм
    Перебирает все аккаунты, пока не удастся залогиниться, если
    аккаунты пошли по второму кругу - вызывает исключение
    """
    account = get_account()
    account_id = account.id
    first = True

    while True:
        if first:
            first = False
        else:
            account = get_account()
            if account.id == account_id:
                raise Exception('All accounts are down')
        try:
            settings.INSTAGRAM_CLIENT = InstagramClient(account)
            account.successful_login()
            break
        except Exception as e:
            account.unsuccessful_login(str(e))


def get_instagram_client():
    """
    Возвращает объект класса Instagram для взаимодействия с ним,
    сделано через этот метод, чтобы при неудачном логине сервер не
    ложился на старте
    :return InstagramClient
    """
    if not settings.INSTAGRAM_CLIENT:
        change_instagram_client()

    return settings.INSTAGRAM_CLIENT


def instagram_exception(func):
    """
    Обрабатывает исключения, возникающие во время работы с Instagram,
    в случае чего перелогиниться или попытается найти другой работающий аккаунт
    """
    def wrapper(*args, **kwargs):

        while True:
            try:
                result = func(*args, **kwargs)
                client = get_instagram_client()
                InstagramLogin.objects.get(id=client.insta_login_id).successful_login()
                break

            except (RateLimitError) as e:
                client = get_instagram_client()
                InstagramLogin.objects.get(id=client.insta_login_id).unsuccessful_login(str(e))
                change_instagram_client()
            except (KeyError) as n:
                client = get_instagram_client()
                InstagramLogin.objects.get(id=client.insta_login_id).unsuccessful_login(str(n))

                try:
                    change_instagram_client()
                    result = func(*args, **kwargs)
                    client = get_instagram_client()
                    InstagramLogin.objects.get(id=client.insta_login_id).successful_login()
                    break
                except Exception as e:
                    client = get_instagram_client()
                    InstagramLogin.objects.get(id=client.insta_login_id).unsuccessful_login()
                    raise Exception(f'KeyError last: {n},\nNew exception: {e}\n, params func:\n{args}\n{kwargs}')

            except Exception as e:
                client = get_instagram_client()
                InstagramLogin.objects.get(id=client.insta_login_id).unsuccessful_login(str(e))

                try:
                    client.relogin()

                except Exception as e:
                    InstagramLogin.objects.get(id=client.insta_login_id).unsuccessful_login(str(e))
                    change_instagram_client()

        return result

    return wrapper


class InstagramClient():

    def __init__(self, insta_login: InstagramLogin) -> None:

        self.instagram = Client()
        self.insta_login_id = insta_login.pk
        # if insta_login.cookie:
        #     self.instagram.load_settings(insta_login.cookie.path)
        self.instagram.login(insta_login.username, insta_login.password, relogin=True)
        # else:
        #     self.instagram.login(insta_login.username, insta_login.password)
        #     insta_login.cookie.save(path_to_cookies(insta_login), ContentFile(''), save=True)
        #     self.instagram.dump_settings(insta_login.cookie.path)
        #     insta_login.save()

        self.instagram.request_timeout = 5

    @instagram_exception
    def relogin(self) -> None:
        insta_login = InstagramLogin.objects.get(id=self.insta_login_id)
        # self.instagram.load_settings(insta_login.cookie.path)
        self.instagram.login(insta_login.username, insta_login.password, relogin=True)
        self.instagram.request_timeout = 7

    def processing_resources_user(self, username: str):
        """Обрабатывает данные пользователя с заданным username с главной страницы и историй"""

        is_updated_set_true(username)

        info = self.get_info(username)
        set_info_about_user(username, info)
        self.processing_resources_from_main_page(username)
        self.processing_resources_form_stories(username)

        update_time(username)

    @instagram_exception
    def get_info(self, username: str):
        """Возвращает основную информация о профиле Instagram в виде nametuple DataAboutUser"""
        user_id = self.instagram.user_id_from_username(username)
        info = self.instagram.user_info(user_id)

        return info

    def processing_resources_from_main_page(self, username: str):
        """Обрабатывает данные пользователя с заданным username с главной страницы"""

        user = UserObject.objects.filter(username=username).first()

        if not user:
            return None

        medias: [] = self._get_medias(username)

        for media in medias:

            if user.medias.get(str(media.pk)) is not None:
                continue

            media_type: str = self._get_media_type_name(media)
            date_time: datetime = self._create_datetime_from_date_and_time(
                media.taken_at.date(),
                media.taken_at.time()
            )

            hashtags: [str] = self._get_hashtags_from_caption(media.caption_text)
            friends: [str] = self._get_media_friends(media)
            link: str = f"https://www.instagram.com/p/{media.code}/"

            user.medias.update({
                str(media.pk): {
                    'type': media_type,
                    'likes': int(media.like_count),
                    'comments': int(media.comment_count),
                    'date': str(date_time),
                    'link': link,
                    'objects': [],
                    'hashtags': hashtags,
                    'friends': friends}
            })

        user.save()

    def processing_resources_form_stories(self, username: str):
        """Обрабатывает данные пользователя с заданным username из историй"""

        user = UserObject.objects.filter(username=username).first()

        if not user:
            return None

        stories: [] = self._get_stories(username)

        for story in stories:

            if user.stories.get(str(story.pk)) is not None:
                continue

            story_type: str = self._get_story_type_name(story)
            date_time: datetime = self._create_datetime_from_date_and_time(
                story.taken_at.date(),
                story.taken_at.time()
            )

            hashtags: [str] = []
            friends: [str] = self._get_story_friends(story)

            user.stories.update({
                str(story.pk): {
                    'type': story_type,
                    'date': str(date_time),
                    'objects': [],
                    'hashtags': hashtags,
                    'friends': friends}
            })

        user.save()

    @instagram_exception
    def _get_stories(self, username: str) -> []:
        """Возвращает все истории пользователя с заданным username"""

        user_id = self.instagram.user_id_from_username(username)
        stories = self.instagram.user_stories(user_id)

        return stories

    @instagram_exception
    def _get_medias(self, username) -> []:
        """Возвращает все ресурсы с главной страницы пользователя с заданным username"""

        user_id = self.instagram.user_id_from_username(username)
        medias = self.instagram.user_medias(user_id, amount=75)

        return medias

    @staticmethod
    def _download_profile_pict(url_pic: str) -> Optional[bytes]:
        """Скачивает фотография профиля Instagram"""
        response = requests.get(url_pic)

        if not response.ok:
            return None

        return response.content

    @staticmethod
    def _get_story_friends(story) -> [str]:
        """Возвращает отмеченных пользователей в истории"""

        friends = []
        for usertag in story.mentions:
            friends.append((dict(dict(usertag).get('user'))['username']))

        return friends

    @staticmethod
    def _get_media_friends(media) -> [str]:
        """Возвращает отмеченных пользователей в медиа"""

        friends = []
        for usertag in media.usertags:
            friends.append((dict(dict(usertag).get('user'))['username']))

        return friends

    @staticmethod
    def _get_media_type_name(media) -> str:
        """Возвращает тип медиа в виде строки"""

        if media.media_type == 1:
            return "photo"
        if media.media_type == 8:
            return "album"

        return media.product_type

    @staticmethod
    def _get_story_type_name(story) -> str:
        """Возвращает тип истории в виде строки"""

        if story.media_type == 1:
            return "photo"

        return story.product_type

    @staticmethod
    def _create_datetime_from_date_and_time(date: datetime.date, time: datetime.time) -> datetime:
        """Создает datetime из date и time"""
        return datetime.datetime(year=date.year, month=date.month, day=date.day,
                                 hour=time.hour, minute=time.minute, second=time.second, microsecond=time.microsecond)

    @staticmethod
    def _get_hashtags_from_caption(caption: str) -> [str]:
        """Возвращает из caption media, используемые в ней хештеги"""

        try:
            hashtags = []
            while caption.find("#"):
                hashtag = ""
                i = caption.index("#")
                while len(caption) > (i + 1) and caption[i + 1] != " " and caption[i + 1] != "\n":
                    hashtag += caption[i + 1]
                    i += 1
                
                hashtag = hashtag.split("#")
                
                for ht in hashtag:
                    hashtags.append(ht.strip())
                caption = caption.replace("#", "", 1)
        except Exception:
            pass

        return hashtags
