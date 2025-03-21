# Generated by Django 5.1.7 on 2025-03-13 21:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('following', models.ManyToManyField(related_name='followers', to='geo_social_app.person')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ap_id', models.TextField(null=True)),
                ('content', models.CharField(max_length=500)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='geo_social_app.person')),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ap_id', models.TextField()),
                ('payload', models.BinaryField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='geo_social_app.person')),
            ],
        ),
    ]
