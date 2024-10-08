# Generated by Django 5.0.6 on 2024-07-12 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0011_alter_menuitem_category_alter_menuitem_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner')], max_length=10, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='type',
            field=models.CharField(choices=[('Veg', 'Veg'), ('Non-Veg', 'Non-Veg')], max_length=10, verbose_name='Type'),
        ),
    ]
