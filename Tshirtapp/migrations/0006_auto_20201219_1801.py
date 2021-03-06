# Generated by Django 3.0.5 on 2020-12-19 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tshirtapp', '0005_order_orderitem_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_id',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_request_id',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_status',
            field=models.CharField(default=False, max_length=30),
        ),
    ]
