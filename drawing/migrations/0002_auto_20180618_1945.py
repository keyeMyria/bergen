# Generated by Django 2.0.6 on 2018-06-18 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drawing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roi',
            name='vectors',
            field=models.CharField(max_length=3000),
        ),
    ]
