# Generated by Django 3.1.7 on 2021-04-14 20:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0005_auto_20210414_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizresult',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
