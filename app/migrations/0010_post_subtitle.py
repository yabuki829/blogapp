# Generated by Django 2.2.27 on 2022-03-07 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='subtitle',
            field=models.CharField(default=2, max_length=100, verbose_name='サブタイトル'),
            preserve_default=False,
        ),
    ]
