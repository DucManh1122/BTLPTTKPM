# Generated by Django 4.1.6 on 2023-05-10 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=255)),
                ("product_id", models.IntegerField()),
                ("content", models.TextField()),
                ("createAt", models.DateField(auto_now_add=True)),
            ],
        ),
    ]