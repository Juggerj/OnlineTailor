# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-10-01 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0005_auto_20170425_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u0438\u044f \u0437\u0430\u044f\u0432\u043a\u0438')),
                ('type', models.CharField(default='', max_length=50, verbose_name='\u0422\u0438\u043f \u0437\u0430\u044f\u0432\u043a\u0438')),
                ('name', models.CharField(default='', max_length=200, verbose_name='\u0418\u043c\u044f')),
                ('phone', models.CharField(default='', max_length=20, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d')),
                ('email', models.EmailField(default='', max_length=100, verbose_name='\u042d\u043b\u0435\u043a\u0442\u0440\u043e\u043d\u043d\u0430\u044f \u043f\u043e\u0447\u0442\u0430')),
                ('is_payed', models.BooleanField(default=False, verbose_name='\u041e\u043f\u043b\u0430\u0442\u0430')),
            ],
            options={
                'verbose_name': '\u0417\u0430\u044f\u0432\u043a\u0430',
                'verbose_name_plural': '\u0417\u0430\u044f\u0432\u043a\u0438',
            },
        ),
        migrations.AlterField(
            model_name='visitor',
            name='time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0432\u0445\u043e\u0434\u0430'),
        ),
    ]
