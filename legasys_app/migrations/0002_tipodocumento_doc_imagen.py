# Generated by Django 4.2.1 on 2023-06-05 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legasys_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipodocumento',
            name='doc_imagen',
            field=models.FileField(null=True, upload_to='', verbose_name='Imagen'),
        ),
    ]