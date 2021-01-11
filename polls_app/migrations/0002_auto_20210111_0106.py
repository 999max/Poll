# Generated by Django 2.2.10 on 2021-01-10 22:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='passed_users',
            field=models.ForeignKey(blank=True, on_delete=models.SET('nobody'), to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='poll',
            name='passed_users',
            field=models.ForeignKey(blank=True, on_delete=models.SET('nobody'), to=settings.AUTH_USER_MODEL),
        ),
    ]
