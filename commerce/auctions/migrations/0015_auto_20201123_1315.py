# Generated by Django 3.1.3 on 2020-11-23 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auto_20201121_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, default='Others', max_length=64),
        ),
    ]