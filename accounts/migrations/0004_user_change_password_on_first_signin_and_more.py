# Generated by Django 4.1.2 on 2022-10-28 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_alter_user_is_verified"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="change_password_on_first_signin",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="is_auto_generate_password",
            field=models.BooleanField(default=False),
        ),
    ]
