# Generated by Django 4.2.4 on 2023-08-28 22:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('factapp', '0003_alter_article_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': 'Article', 'verbose_name_plural': 'Articles'},
        ),
    ]
