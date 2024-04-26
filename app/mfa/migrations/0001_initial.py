# Generated by Django 4.2.4 on 2024-04-24 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User_Keys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('properties', models.JSONField(null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('key_type', models.CharField(default='TOTP', max_length=25)),
                ('enabled', models.BooleanField(default=True)),
                ('expires', models.DateTimeField(blank=True, default=None, null=True)),
                ('last_used', models.DateTimeField(blank=True, default=None, null=True)),
                ('owned_by_enterprise', models.BooleanField(blank=True, default=None, null=True)),
            ],
        ),
    ]
