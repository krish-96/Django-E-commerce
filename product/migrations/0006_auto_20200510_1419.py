# Generated by Django 2.2.9 on 2020-05-10 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20200510_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='status',
            field=models.CharField(choices=[('False', 'False'), ('True', 'True')], max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('False', 'False'), ('True', 'True')], max_length=10),
        ),
    ]
