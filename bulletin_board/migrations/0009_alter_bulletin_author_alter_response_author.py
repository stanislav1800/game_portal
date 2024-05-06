# Generated by Django 5.0.2 on 2024-05-04 21:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin_board', '0008_alter_response_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bulletin_board.profile'),
        ),
        migrations.AlterField(
            model_name='response',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bulletin_board.profile'),
        ),
    ]
