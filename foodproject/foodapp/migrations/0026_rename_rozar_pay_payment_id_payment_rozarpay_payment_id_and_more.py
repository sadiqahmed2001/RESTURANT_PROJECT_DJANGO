# Generated by Django 5.0.6 on 2024-07-19 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0025_alter_menuitem_category_alter_menuitem_type_order_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='rozar_pay_Payment_id',
            new_name='rozarpay_Payment_id',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='rozar_pay_order_id',
            new_name='rozarpay_order_id',
        ),
    ]
