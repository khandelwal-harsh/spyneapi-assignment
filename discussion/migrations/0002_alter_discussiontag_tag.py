# Generated by Django 3.2.15 on 2024-07-27 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussiontag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='discussion.tag'),
        ),
    ]
