# Generated by Django 5.0.2 on 2024-05-01 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin_board', '0007_alter_response_unique_together_alter_response_author'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='response',
            unique_together={('bulletin', 'author')},
        ),
    ]