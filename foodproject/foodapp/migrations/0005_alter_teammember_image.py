# Generated by Django 5.0.6 on 2024-07-10 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0004_alter_teammember_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammember',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='posts/'),
        ),
    ]