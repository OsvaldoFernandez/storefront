# Generated by Django 3.2.8 on 2021-10-10 02:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20211009_0329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='membership',
        ),
    ]
