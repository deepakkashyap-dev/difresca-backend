# Generated by Django 4.1.10 on 2024-01-01 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_homepageblock_sequence_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]