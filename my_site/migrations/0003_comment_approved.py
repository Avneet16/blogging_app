# Generated by Django 2.2.4 on 2020-02-15 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_site', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
