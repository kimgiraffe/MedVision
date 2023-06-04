# Generated by Django 4.2 on 2023-05-20 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DrugInfo",
            fields=[
                (
                    "drugNo",
                    models.DecimalField(
                        decimal_places=0,
                        max_digits=9,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("drugName", models.CharField(max_length=25)),
                ("drugEffect", models.CharField(max_length=50)),
                ("component", models.CharField(max_length=50)),
                ("quantity", models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name="PillData",
            fields=[
                (
                    "drugNo",
                    models.DecimalField(
                        decimal_places=0,
                        max_digits=9,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("pillShape", models.TextField(max_length=6)),
                ("pillColor", models.TextField(max_length=20)),
                ("pillText", models.TextField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Prescription",
            fields=[
                (
                    "prescId",
                    models.DecimalField(
                        decimal_places=0,
                        max_digits=13,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("prescDate", models.DateField(default="")),
                ("dispensary", models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name="User",
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
                ("userId", models.CharField(max_length=12, unique=True)),
                ("userPassword", models.CharField(max_length=20)),
                (
                    "userRealName",
                    models.CharField(blank=True, default="", max_length=10),
                ),
                ("userEmail", models.EmailField(max_length=25, unique=True)),
                ("userRegisterDatetime", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Schedule",
            fields=[
                ("startDate", models.DateField(default="")),
                ("endDate", models.DateField(default="")),
                (
                    "prescription",
                    models.ForeignKey(
                        db_column="prescId",
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="schedules",
                        serialize=False,
                        to="users.prescription",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="prescription",
            name="user",
            field=models.ForeignKey(
                db_column="userId",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="prescriptions",
                to="users.user",
            ),
        ),
        migrations.CreateModel(
            name="PrescDetail",
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
                ("dosagePerOnce", models.DecimalField(decimal_places=2, max_digits=6)),
                ("dailyDose", models.IntegerField()),
                ("totalDosingDays", models.IntegerField()),
                (
                    "drugInfo",
                    models.ForeignKey(
                        db_column="drugNo",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="prescDetail",
                        to="users.druginfo",
                    ),
                ),
                (
                    "prescription",
                    models.ForeignKey(
                        db_column="prescId",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="prescDetail",
                        to="users.prescription",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DrugHour",
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
                ("hour", models.TimeField()),
                (
                    "prescDetail",
                    models.ForeignKey(
                        db_column="prescDetail",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="drugHour",
                        to="users.prescdetail",
                    ),
                ),
                (
                    "schedule",
                    models.ForeignKey(
                        db_column="schedule",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="drugHour",
                        to="users.schedule",
                    ),
                ),
            ],
        ),
    ]