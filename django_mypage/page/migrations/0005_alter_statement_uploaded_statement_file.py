# Generated by Django 4.0.1 on 2022-12-11 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0004_rename_listofstatementfiles_statement_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statement',
            name='uploaded_statement_file',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]