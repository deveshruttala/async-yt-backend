# Generated by Django 5.1.1 on 2024-10-08 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_videodata_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videodata',
            name='thumb_url',
            field=models.URLField(blank=True, default=None, null=True),
        ),
    ]
