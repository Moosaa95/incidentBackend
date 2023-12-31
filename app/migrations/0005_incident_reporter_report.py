# Generated by Django 4.2.5 on 2023-09-13 16:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_incident_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='reporter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('details', models.TextField()),
                ('status', models.CharField(choices=[('ongoing', 'Ongoing'), ('investigating', 'Investigating'), ('resolved', 'Resolved')], max_length=20)),
                ('incident', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.incident')),
            ],
        ),
    ]
