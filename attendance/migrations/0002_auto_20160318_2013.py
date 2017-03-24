# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-18 11:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_join', models.BooleanField(default=False)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Practice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('practice_dt', models.DateField()),
                ('create_dt', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('no', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=40)),
                ('author', models.CharField(max_length=60)),
                ('play_time', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='practice',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.Song'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='practice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.Practice'),
        ),
    ]
