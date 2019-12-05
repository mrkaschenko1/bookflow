# Generated by Django 3.0 on 2019-12-05 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
        ('accounts', '0003_auto_20191206_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='books',
            field=models.ManyToManyField(blank=True, related_name='book', to='book.Book'),
        ),
    ]
