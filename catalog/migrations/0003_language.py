# Generated by Django 2.1.2 on 2018-10-02 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20181002_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('eng', 'English'), ('fre', 'French'), ('ger', 'German'), ('spa', 'Spanish'), ('por', 'Portuguese'), ('ita', 'Italian'), ('chi', 'Chinese'), ('can', 'Canadian')], help_text='Pick a language', max_length=100)),
            ],
            options={
                'ordering': ['language'],
            },
        ),
    ]
