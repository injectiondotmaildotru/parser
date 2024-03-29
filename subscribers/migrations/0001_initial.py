# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-06-09 11:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('scraping', '0004_site_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100, unique=True, verbose_name='E-mail')),
                ('password', models.CharField(max_length=100, verbose_name='Пароль')),
                ('is_active', models.BooleanField(default=True, verbose_name='Получать рассылку?')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.City', verbose_name='Город')),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.Speciality', verbose_name='Специальность')),
            ],
            options={
                'verbose_name': 'Подписчик',
                'verbose_name_plural': 'Подписчики',
            },
        ),
    ]
