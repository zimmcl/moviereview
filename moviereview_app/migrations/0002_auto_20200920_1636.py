# Generated by Django 3.1.1 on 2020-09-20 19:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('moviereview_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='content',
            new_name='synopsis',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='dislikes',
            new_name='votes',
        ),
        migrations.RemoveField(
            model_name='article',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='article',
            name='users_reactions',
        ),
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
