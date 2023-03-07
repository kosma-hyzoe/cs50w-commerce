# Generated by Django 4.1.7 on 2023-03-07 09:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_seller_listing_seller_id_listing_current_bid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='seller_id',
            new_name='seller',
        ),
        migrations.AddField(
            model_name='listing',
            name='date_posted',
            field=models.DateField(default=datetime.datetime(2023, 3, 7, 9, 36, 33, 173387)),
            preserve_default=False,
        ),
    ]
