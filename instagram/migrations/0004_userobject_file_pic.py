# Generated by Django 3.2.9 on 2022-02-05 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0003_alter_userobject_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='userobject',
            name='file_pic',
            field=models.ImageField(blank=True, null=True, upload_to='pic/', verbose_name='Хранит иконку профиля пользователя'),
        ),
    ]
