# Generated by Django 5.1.7 on 2025-05-02 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=120, unique=True)),
                ('password', models.CharField(max_length=120)),
                ('school_student', models.BooleanField(default=False)),
            ],
        ),
    ]
