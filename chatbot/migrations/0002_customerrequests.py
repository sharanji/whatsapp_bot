# Generated by Django 4.1.6 on 2023-02-21 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerRequests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('contact_number', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
