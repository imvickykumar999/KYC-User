# Generated by Django 5.0.1 on 2024-08-04 16:47

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='likedislike',
            unique_together={('post', 'user')},
        ),
    ]
