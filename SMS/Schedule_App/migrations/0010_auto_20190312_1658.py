# Generated by Django 2.1.7 on 2019-03-12 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule_App', '0009_auto_20190312_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='profile_pic.png', upload_to='profile_pics'),
        ),
    ]
