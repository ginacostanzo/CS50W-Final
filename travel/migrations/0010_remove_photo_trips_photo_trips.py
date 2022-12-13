# Generated by Django 4.1.1 on 2022-12-03 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0009_alter_trip_status_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='trips',
        ),
        migrations.AddField(
            model_name='photo',
            name='trips',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='trip', to='travel.trip'),
        ),
    ]