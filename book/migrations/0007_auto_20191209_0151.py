# Generated by Django 3.0 on 2019-12-08 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_auto_20191206_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinfo',
            name='small_pic_url',
            field=models.URLField(blank=True, max_length=1000),
        ),
    ]