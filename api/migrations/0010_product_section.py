# Generated by Django 4.1.10 on 2024-02-06 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_product_choose_relation_alter_banners_relation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='section',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_active': True, 'type__in': ['CATEGORY_PRODUCT']}, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.homepageblock'),
        ),
    ]
