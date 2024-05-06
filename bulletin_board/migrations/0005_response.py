# Generated by Django 5.0.2 on 2024-05-01 21:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin_board', '0004_category_subscribers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bulletin_board.profile')),
                ('bulletin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bulletin_board.bulletin')),
            ],
        ),
    ]
