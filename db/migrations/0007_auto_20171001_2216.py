# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-10-01 17:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0006_auto_20171001_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 1, 22, 16, 7, 818000), verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u0438\u044f \u0437\u0430\u044f\u0432\u043a\u0438'),
        ),
    ]