# Generated by Django 2.1.7 on 2019-03-13 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.SmallIntegerField(verbose_name='Rating')),
                ('review_text', models.TextField(verbose_name='Review text')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='hotel.Hotel')),
            ],
        ),
    ]
