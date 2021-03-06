# Generated by Django 3.1.1 on 2020-09-27 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0009_auto_20200920_1557'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descriptions', models.TextField(blank=True)),
                ('base_product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='models.baseproduct')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images_product', to='models.baseproduct')),
            ],
        ),
    ]
