# Generated by Django 2.2.9 on 2020-05-16 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20200514_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmessage',
            name='status',
            field=models.EmailField(choices=[('Closed', 'Closed'), ('Read', 'Read'), ('New', 'New')], default='New', max_length=10),
        ),
        migrations.AlterField(
            model_name='setting',
            name='status',
            field=models.CharField(choices=[('False', 'False'), ('True', 'True')], max_length=10),
        ),
    ]
