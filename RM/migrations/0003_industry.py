# Generated by Django 4.2 on 2023-04-12 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RM', '0002_items'),
    ]

    operations = [
        migrations.CreateModel(
            name='industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IndustryName', models.CharField(max_length=200)),
                ('Category', models.CharField(max_length=200)),
                ('Type', models.CharField(max_length=200)),
                ('Location', models.CharField(max_length=200)),
                ('Phone', models.IntegerField()),
            ],
        ),
    ]
