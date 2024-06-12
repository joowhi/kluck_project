# Generated by Django 5.0.6 on 2024-06-12 06:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("gpt_prompts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="LuckMessage",
            fields=[
                ("msg_id", models.AutoField(primary_key=True, serialize=False)),
                ("luck_date", models.CharField(blank=True, max_length=8, null=True)),
                ("category", models.CharField(blank=True, max_length=50, null=True)),
                ("attribute1", models.CharField(blank=True, max_length=50, null=True)),
                ("attribute2", models.CharField(blank=True, max_length=50, null=True)),
                ("luck_msg", models.TextField(blank=True, null=True)),
                (
                    "gpt_id",
                    models.ForeignKey(
                        db_column="gpt_id",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="gpt_prompts.gptprompt",
                    ),
                ),
            ],
        ),
    ]
