# Generated by Django 4.2.16 on 2025-03-16 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0004_alter_command_command_delete_executionresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('os', models.CharField(max_length=50)),
                ('format', models.CharField(max_length=50)),
                ('file_path', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
