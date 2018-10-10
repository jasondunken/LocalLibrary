# Generated by Django 2.1.2 on 2018-10-02 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SomeTypicalModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('awesome_field', models.CharField(help_text='Example of what to enter', max_length=200)),
            ],
            options={
                'verbose_name': 'EvenMoreAwesomeName',
                'ordering': ['-awesome_field'],
            },
        ),
    ]