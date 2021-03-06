# Generated by Django 2.0.7 on 2018-07-12 17:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drawing', '0002_auto_20180704_1616'),
        ('bioconverter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OutFlower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('path', models.CharField(max_length=500)),
                ('outputtype', models.CharField(max_length=200)),
                ('channel', models.CharField(max_length=100)),
                ('defaultsettings', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='OutFlowRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('settings', models.CharField(max_length=1000)),
                ('inputvid', models.IntegerField()),
                ('outflower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bioconverter.OutFlower')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drawing.Sample')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
