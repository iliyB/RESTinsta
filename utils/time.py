from django.utils import timezone


def edit_current_time():
    return timezone.localtime(timezone.now())