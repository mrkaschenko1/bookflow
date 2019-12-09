# Generated by Django 3.0 on 2019-12-08 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_profile_books'),
        ('book', '0007_auto_20191209_0151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shelf',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shelves', to='accounts.Profile'),
        ),
    ]
