# Generated by Django 4.2.2 on 2023-11-24 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_profile_profile_pic_alter_bubble_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='profil_pic'),
        ),
    ]
