# Generated by Django 2.2 on 2019-05-08 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='blank.jpg', upload_to='profile_pics'),
        ),
    ]