# Generated by Django 2.1.7 on 2019-03-04 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_interface', '0004_auto_20190303_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pin',
            field=models.IntegerField(max_length=6, unique=True),
        ),
    ]