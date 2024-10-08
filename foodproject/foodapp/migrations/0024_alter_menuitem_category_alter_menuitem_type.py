# Generated by Django 5.0.6 on 2024-07-12 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0023_alter_menuitem_category_alter_menuitem_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.PositiveIntegerField(choices=[(1, 'BREAKFAST'), (2, 'LUNCH'), (3, 'DINNER')], verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='type',
            field=models.PositiveIntegerField(choices=[(1, 'VEG'), (2, 'NON-VEG'), (3, 'HOTDRINKS'), (4, 'COLDDRINKS')], default=1, verbose_name='type'),
        ),
    ]
