# Generated by Django 2.1.2 on 2018-10-16 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20181011_1543'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name', 'first_name'], 'permissions': (('can_create_author', 'can_create_author'),)},
        ),
    ]
