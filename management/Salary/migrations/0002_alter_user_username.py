# Generated by Django 4.0.5 on 2022-06-24 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Salary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]
