# Generated by Django 2.2.9 on 2020-05-11 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20200511_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmessage',
            name='status',
            field=models.EmailField(choices=[('Closed', 'Closed'), ('Read', 'Read'), ('New', 'New')], default='New', max_length=10),
        ),
    ]
