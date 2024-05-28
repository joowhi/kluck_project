# Generated by Django 5.0.6 on 2024-05-27 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admins", "0006_rename_admin_pw_admin_password_admin_last_login"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="admin",
            name="admin_id",
        ),
        migrations.RemoveField(
            model_name="admin",
            name="permission",
        ),
        migrations.AlterField(
            model_name="admin",
            name="password",
            field=models.CharField(max_length=128, verbose_name="password"),
        ),
    ]
