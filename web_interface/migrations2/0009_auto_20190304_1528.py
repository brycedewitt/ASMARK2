# Generated by Django 2.1.7 on 2019-03-04 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_interface', '0008_auto_20190304_1332'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pour',
            options={'ordering': ['volume'], 'verbose_name_plural': 'Pours'},
        ),
        migrations.AlterField(
            model_name='beverage',
            name='gpio_pin',
            field=models.IntegerField(unique=True),
        ),
    ]