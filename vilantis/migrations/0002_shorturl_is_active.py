# Generated by Django 3.1.5 on 2021-01-30 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vilantis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shorturl',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
    ]