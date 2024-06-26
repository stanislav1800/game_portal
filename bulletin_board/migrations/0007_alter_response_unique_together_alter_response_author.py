# Generated by Django 5.0.2 on 2024-05-01 21:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin_board', '0006_alter_response_author_alter_response_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='response',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='response',
            name='author',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='bulletin_board.profile'),
        ),
    ]
