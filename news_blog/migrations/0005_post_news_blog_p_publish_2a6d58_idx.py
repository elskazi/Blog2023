# Generated by Django 4.1.7 on 2023-03-17 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_blog', '0004_post_tags'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-publish'], name='news_blog_p_publish_2a6d58_idx'),
        ),
    ]