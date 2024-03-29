# Generated by Django 4.1.10 on 2024-01-01 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_banners'),
    ]

    operations = [
        migrations.AddField(
            model_name='banners',
            name='Banner_image',
            field=models.ImageField(default='', upload_to='images/banner/'),
        ),
        migrations.AddField(
            model_name='banners',
            name='Banner_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='banners',
            name='button_background',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='banners',
            name='button_background_hover',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='banners',
            name='button_text',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='banners',
            name='button_text_color',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='banners',
            name='button_text_color_hover',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='banners',
            name='relation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.homepageblock'),
        ),
        migrations.AddField(
            model_name='banners',
            name='width',
            field=models.CharField(choices=[('3', '25 %'), ('6', '50 %'), ('9', '75 %'), ('12', 'full')], default='12', max_length=100),
        ),
    ]
