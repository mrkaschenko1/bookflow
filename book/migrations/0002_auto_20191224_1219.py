# Generated by Django 3.0 on 2019-12-24 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20191216_0012'),
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilebookinfo',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_books', to='accounts.Profile'),
        ),
    ]