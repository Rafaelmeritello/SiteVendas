# Generated by Django 3.2 on 2021-04-30 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_produto_subcategoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='descricao',
            field=models.TextField(default='', max_length=1500),
        ),
    ]