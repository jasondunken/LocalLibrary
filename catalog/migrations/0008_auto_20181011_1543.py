# Generated by Django 2.1.2 on 2018-10-11 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20181011_1428'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'set_as_book_returned'),)},
        ),
    ]
