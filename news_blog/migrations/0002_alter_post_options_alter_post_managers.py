# Generated by Django 4.1.7 on 2023-03-13 10:06

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('news_blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-publish',)},
        ),
        migrations.AlterModelManagers(
            name='post',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
