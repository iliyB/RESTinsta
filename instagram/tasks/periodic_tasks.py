from configs.celery import app
from instagram.models import UserObject
from instagram.service.api_insta import InstagramClient, get_instagram_client
from instagram.tasks.tasks import add_data_about_user


@app.task
def update_data_about_users():
    """Обновляет данные пользователей из социальной сети"""
    usernames = UserObject.objects.exclude(activate=False).values_list('username', flat=True)

    for username in usernames:
        add_data_about_user.delay(username)
