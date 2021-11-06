# Generated by Django 3.2.8 on 2021-11-02 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_alter_customer_birth_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'Can cancel order')]},
        ),
        migrations.AlterField(
            model_name='customer',
            name='membership',
            field=models.CharField(choices=[('B', 'Bronze'), ('S', 'Silver'), ('G', 'Gold')], default='B', max_length=1),
        ),
    ]