# Generated by Django 3.1.7 on 2021-05-02 11:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("forms", "0004_form_redirect_url"),
    ]

    operations = [
        migrations.CreateModel(
            name="FormMailSettings",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email_address", models.EmailField(max_length=254)),
                (
                    "form",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="forms.form"
                    ),
                ),
            ],
        ),
    ]