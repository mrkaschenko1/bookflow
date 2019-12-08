# Generated by Django 3.0 on 2019-12-06 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_profile_books'),
        ('book', '0004_shelf_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shelf',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shelf', to='accounts.Profile'),
        ),
    ]
