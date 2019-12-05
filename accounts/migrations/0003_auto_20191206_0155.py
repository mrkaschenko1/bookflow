# Generated by Django 3.0 on 2019-12-05 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
        ('accounts', '0002_profile_books'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='books',
            field=models.ManyToManyField(null=True, related_name='book', to='book.Book'),
        ),
    ]
