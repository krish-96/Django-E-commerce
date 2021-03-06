# Generated by Django 2.2.9 on 2020-05-11 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20200511_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmessage',
            name='status',
            field=models.EmailField(choices=[('New', 'New'), ('Read', 'Read'), ('Closed', 'Closed')], default='New', max_length=10),
        ),
        migrations.AlterField(
            model_name='setting',
            name='status',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False')], max_length=10),
        ),
    ]
