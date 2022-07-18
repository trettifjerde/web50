# Generated by Django 4.0.6 on 2022-07-18 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_remove_category_listings_listing_category_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bid',
            options={'ordering': ['-price']},
        ),
        migrations.AddField(
            model_name='category',
            name='color',
            field=models.CharField(blank=True, max_length=7),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='listings', to='auctions.category'),
        ),
    ]
