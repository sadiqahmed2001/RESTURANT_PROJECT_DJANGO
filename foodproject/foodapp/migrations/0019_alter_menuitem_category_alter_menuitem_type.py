# Generated by Django 5.0.6 on 2024-07-12 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0018_alter_menuitem_category_alter_menuitem_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.CharField(choices=[(1, 'Breakfast'), (2, 'Lunch'), (3, 'Dinner')], max_length=10, verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='type',
            field=models.CharField(choices=[(1, 'Veg'), (2, 'Non-Veg'), (3, 'HotDrinks'), (4, 'ColdDrinks')], default=None, max_length=10, verbose_name='type'),
        ),
    ]
