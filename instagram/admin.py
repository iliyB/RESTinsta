from django.contrib import admin

from instagram.models import UserObject, InstagramLogin


admin.site.register(UserObject)
admin.site.register(InstagramLogin)
