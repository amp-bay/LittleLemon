# Generated by Django 5.1.4 on 2024-12-21 03:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonApiApp', '0004_alter_cart_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together={('user', 'menuitem')},
        ),
    ]
