# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('content', models.CharField(max_length=500, verbose_name='Message')),
                ('pub_date', models.DateTimeField(verbose_name='Date sent')),
                ('mess_receiver', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='Receiver', on_delete=models.CASCADE)),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='Sender', on_delete=models.CASCADE)),
            ],
        ),
    ]
