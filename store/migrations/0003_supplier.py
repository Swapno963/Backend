# Generated by Django 5.1.3 on 2024-11-25 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_delete_supplier_card_is_feature_menu_card_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
