# Generated by Django 3.1.1 on 2020-09-21 02:51

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('moviereview_app', '0004_article_url_embed'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Article',
            new_name='Content',
        ),
    ]
