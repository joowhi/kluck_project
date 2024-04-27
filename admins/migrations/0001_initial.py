# Generated by Django 5.0.4 on 2024-04-27 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Admin",
            fields=[
                ("admins_id", models.AutoField(primary_key=True, serialize=False)),
                ("admin_id", models.CharField(blank=True, max_length=30, null=True)),
                ("admin_user", models.CharField(blank=True, max_length=30, null=True)),
                ("cell_num", models.CharField(blank=True, max_length=11, null=True)),
                ("email", models.CharField(blank=True, max_length=50, null=True)),
                ("create_date", models.CharField(blank=True, max_length=8, null=True)),
                ("permission", models.CharField(blank=True, max_length=30, null=True)),
                ("user_pw", models.CharField(blank=True, max_length=100, null=True)),
                ("adms_id", models.IntegerField(null=True)),
            ],
        ),
    ]
