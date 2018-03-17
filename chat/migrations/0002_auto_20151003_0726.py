# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(to=settings.AUTH_USER_MODEL, serialize=False, primary_key=True, auto_created=True, parent_link=True, on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='message',
            name='mess_receiver',
            field=models.ForeignKey(related_name='Receiver', to='chat.User', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(related_name='Sender', to='chat.User', on_delete=models.CASCADE),
        ),
    ]
