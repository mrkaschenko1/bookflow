# Generated by Django 3.0 on 2019-12-05 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shelf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('books', models.ManyToManyField(blank=True, related_name='shelves', to='book.Book')),
            ],
        ),
    ]
