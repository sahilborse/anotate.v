# Generated by Django 5.1.3 on 2024-11-14 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('column_data', models.JSONField(blank=True, help_text='Store column data in JSON format', null=True)),
            ],
        ),
    ]
