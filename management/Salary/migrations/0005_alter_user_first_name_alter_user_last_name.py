# Generated by Django 4.0.5 on 2022-06-24 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Salary', '0004_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=255),
        ),
    ]
