# Generated by Django 3.2 on 2021-04-29 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_produto_oficial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produto',
            name='oficial',
        ),
        migrations.AddField(
            model_name='produto',
            name='descricao',
            field=models.TextField(default='', max_length=350),
        ),
    ]
