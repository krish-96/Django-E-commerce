# Generated by Django 2.2.9 on 2020-05-11 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_auto_20200510_1726'),
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
