# Generated by Django 5.1.3 on 2024-11-28 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_blacklistedtoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blacklistedtoken',
            name='token',
            field=models.CharField(max_length=512, unique=True),
        ),
    ]