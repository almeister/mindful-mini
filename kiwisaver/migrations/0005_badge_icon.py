# Generated by Django 5.1.2 on 2024-10-22 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiwisaver', '0004_alter_fund_badges_alter_fund_companies_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='badge',
            name='icon',
            field=models.ImageField(null=True, upload_to='badges'),
        ),
    ]
