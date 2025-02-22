# Generated by Django 4.1 on 2025-02-06 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("gestion", "0009_persona_user"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="alumno",
            options={},
        ),
        migrations.AlterField(
            model_name="alumno",
            name="persona",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="gestion.persona"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="alumno",
            unique_together={("persona", "curso", "ano_lectivo")},
        ),
    ]
