from django.core.files.base import ContentFile

from instagram.models import UserObject
from utils.time import edit_current_time


def update_time(username: str) -> None:
    """Обновляет время последнего обновления данных пользователя с данным username"""
    user = UserObject.objects.get(username=username)
    user.last_update = edit_current_time()
    user.is_updated = False
    user.save()

def is_updated_set_true(username: str) -> None:
    """Устанавливает параметр, отвечающий за указание обновляются ли данные о пользователе, в значение True"""
    user = UserObject.objects.get(username=username)
    user.is_updated = True
    user.save()

def set_info_about_user(username: str, info, pic) -> None:
    """Сохраняет основную информация об аккаунте Instagram"""
    user = UserObject.objects.get(username=username)

    user.id_insta = info.pk
    user.full_name = info.full_name
    user.is_private = info.is_private
    user.media_count = info.media_count
    user.follower_count = info.follower_count
    user.following_count = info.following_count
    user.biography = info.biography
    user.external_link = info.external_url
    user.email = info.public_email
    user.phone = info.contact_phone_number
    user.is_business = info.is_business
    user.business_category = info.business_category_name
    user.instagram_link = "https://www.instagram.com/" + username + "/"
    if pic is not None:
        user.pic.save(f"account_pic_{username}.jpg", ContentFile(pic), save=True)
    user.save()