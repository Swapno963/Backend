# Generated by Django 5.1.3 on 2024-11-23 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='is_superuser',
            new_name='is_admin',
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_superadmin',
            field=models.BooleanField(default=False),
        ),
    ]
