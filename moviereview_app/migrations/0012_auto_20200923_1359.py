# Generated by Django 3.1.1 on 2020-09-23 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviereview_app', '0011_auto_20200923_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(default='media/Other/your-image-here.jpg', upload_to='media/'),
        ),
    ]
