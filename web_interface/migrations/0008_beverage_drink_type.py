# Generated by Django 2.1.7 on 2019-03-05 03:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_interface', '0007_drinktype'),
    ]

    operations = [
        migrations.AddField(
            model_name='beverage',
            name='drink_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web_interface.DrinkType'),
        ),
    ]