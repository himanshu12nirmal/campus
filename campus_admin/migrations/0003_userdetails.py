# Generated by Django 4.1.7 on 2023-05-01 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campus_admin', '0002_alter_newuser_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'UserDetails',
            },
        ),
    ]
