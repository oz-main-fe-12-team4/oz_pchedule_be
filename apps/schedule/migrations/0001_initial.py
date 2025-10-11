# apps/schedule/migrations/0001_initial.py
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("user", "0001_initial"),  # User 모델 기준, 필요시 마지막 migration으로 변경
    ]

    operations = [
        # Category 테이블
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True)),
            ],
            options={
                "db_table": "category",
            },
        ),
        # Weekday 테이블
        migrations.CreateModel(
            name="Weekday",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=2, unique=True)),
                ("name", models.CharField(max_length=10)),
            ],
            options={
                "db_table": "weekday",
            },
        ),
        # Schedule 테이블
        migrations.CreateModel(
            name="Schedule",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=100)),
                ("start_period", models.DateTimeField(blank=True, null=True)),
                ("end_period", models.DateTimeField(blank=True, null=True)),
                (
                    "priority",
                    models.CharField(
                        choices=[
                            ("긴급", "긴급"),
                            ("높음", "높음"),
                            ("중간", "중간"),
                            ("낮음", "낮음"),
                            ("보류", "보류"),
                        ],
                        default="중간",
                        max_length=10,
                    ),
                ),
                (
                    "share_type",
                    models.CharField(
                        choices=[("비공개", "비공개"), ("전체공개", "전체공개")], default="비공개", max_length=10
                    ),
                ),
                ("is_someday", models.BooleanField(default=False)),
                ("is_recurrence", models.BooleanField(default=False)),
                ("is_completed", models.BooleanField(default=False)),
                ("is_reported", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="schedule.category"
                    ),
                ),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="user.user")),
            ],
            options={
                "db_table": "schedule",
            },
        ),
        # RecurrenceRule 테이블
        migrations.CreateModel(
            name="RecurrenceRule",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "recurrence_type",
                    models.CharField(
                        choices=[
                            ("DAILY", "Daily"),
                            ("WEEKLY", "Weekly"),
                            ("MONTHLY", "Monthly"),
                            ("YEARLY", "Yearly"),
                        ],
                        max_length=10,
                    ),
                ),
                ("month_of_year", models.PositiveIntegerField(blank=True, null=True)),
                ("day_of_month", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "schedule",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recurrence_rule",
                        to="schedule.schedule",
                    ),
                ),
            ],
            options={
                "db_table": "recurrence_rule",
            },
        ),
        # ManyToManyField for RecurrenceRule.weekdays
        migrations.AddField(
            model_name="recurrencerule",
            name="weekdays",
            field=models.ManyToManyField(blank=True, to="schedule.Weekday"),
        ),
        # DetailSchedule 테이블
        migrations.CreateModel(
            name="DetailSchedule",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True)),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                ("is_completed", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "schedule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="detail_schedule",
                        to="schedule.schedule",
                    ),
                ),
            ],
            options={
                "db_table": "detail_schedule",
            },
        ),
    ]
