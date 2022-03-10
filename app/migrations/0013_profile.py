# Generated by Django 2.2.27 on 2022-03-10 06:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0012_delete_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=50, verbose_name='ニックネーム')),
                ('profile', models.CharField(blank=True, max_length=50, null=True, verbose_name='profile')),
                ('Twitter', models.CharField(blank=True, max_length=100, null=True, verbose_name='Twitter')),
                ('Qiita', models.CharField(blank=True, max_length=100, null=True, verbose_name='キータ ')),
                ('Link', models.CharField(blank=True, max_length=100, null=True, verbose_name='link')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images', verbose_name='画像')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]