# Generated by Django 2.1.7 on 2019-03-16 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190316_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='end_at',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='start_at',
            field=models.DateField(null=True),
        ),
    ]