from typing import Optional

from instagram.models import InstagramLogin


def get_account() -> Optional[InstagramLogin]:
    """
    Возвращает аккаунт инстаграм для логина.
    Сначала берет работающие аккаунты с позднейшей попыткой входа,
    если таких нет - неработающие аккаунты с позднейшей попыткой входа.
    """
    account = InstagramLogin.objects.filter(worked=True, active=True).order_by('last_attempt').first()

    if not account:
        account = InstagramLogin.objects.filter(worked=False, active=True).order_by('last_attempt').first()

    return account