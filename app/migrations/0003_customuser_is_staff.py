# Generated by Django 4.2.5 on 2023-09-10 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_location_incident'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
    ]
