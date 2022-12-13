# Generated by Django 4.1.1 on 2022-12-01 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0004_alter_trip_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='title',
            field=models.TextField(default='title', max_length=500),
        ),
        migrations.AlterField(
            model_name='trip',
            name='img',
            field=models.ImageField(upload_to='media'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='location',
            field=models.CharField(max_length=100),
        ),
    ]
