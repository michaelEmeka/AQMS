# Generated by Django 5.1.4 on 2025-01-12 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_address', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('last_filled', models.DateTimeField(auto_now_add=True)),
                ('is_pumping', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('water_level', models.IntegerField(default=0)),
            ],
        ),
    ]
