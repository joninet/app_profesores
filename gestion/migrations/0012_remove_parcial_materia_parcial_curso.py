# Generated by Django 4.1 on 2025-02-06 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("gestion", "0011_parcial_nota"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="parcial",
            name="materia",
        ),
        migrations.AddField(
            model_name="parcial",
            name="curso",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="gestion.curso",
            ),
            preserve_default=False,
        ),
    ]
