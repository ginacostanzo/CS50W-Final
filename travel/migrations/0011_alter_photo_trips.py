# Generated by Django 4.1.1 on 2022-12-03 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0010_remove_photo_trips_photo_trips'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='trips',
            field=models.ForeignKey(default=32, on_delete=django.db.models.deletion.CASCADE, related_name='trip', to='travel.trip'),
        ),
    ]
