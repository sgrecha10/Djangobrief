# Generated by Django 3.1.1 on 2020-09-16 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0005_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='upfile',
            field=models.FileField(upload_to='documents/'),
        ),
    ]