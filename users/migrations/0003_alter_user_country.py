# Generated by Django 4.2.2 on 2024-05-17 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_token_alter_user_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, help_text='Введите свою страну', max_length=255, null=True, verbose_name='Страна'),
        ),
    ]
