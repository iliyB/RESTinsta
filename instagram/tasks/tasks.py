from configs.celery import app
from instagram.service.api_insta import InstagramClient, get_instagram_client


@app.task
def add_data_about_user(username: str):
    """Обрабатывает информацию о пользователи из социальной сети при инициализации этого пользователя"""

    instagramClient = get_instagram_client()
    instagramClient.processing_resources_user(username)
