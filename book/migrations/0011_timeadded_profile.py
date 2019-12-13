# Generated by Django 3.0 on 2019-12-11 22:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_profile_books'),
        ('book', '0010_timeadded'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeadded',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile'),
        ),
    ]