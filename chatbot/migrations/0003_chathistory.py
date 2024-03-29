# Generated by Django 4.1.6 on 2023-02-22 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0002_customerrequests'),
    ]

    operations = [
        migrations.CreateModel(
            name='chatHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_query', models.TextField()),
                ('bot_response', models.TextField()),
                ('contact_number', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
