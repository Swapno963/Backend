# Generated by Django 5.1.3 on 2024-11-23 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_supplierprofile_street_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplierprofile',
            name='documents',
            field=models.ImageField(blank=True, null=True, upload_to='supplier/documents/'),
        ),
    ]
