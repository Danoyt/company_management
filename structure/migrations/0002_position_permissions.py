# Generated by Django 5.1.3 on 2024-11-22 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('structure', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='permissions',
            field=models.ManyToManyField(related_name='positions', to='auth.permission'),
        ),
    ]