# Generated by Django 2.2.9 on 2020-01-03 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0005_post_books'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='books',
            field=models.ManyToManyField(null=True, related_name='posts', to='book.BookInfo'),
        ),
    ]
