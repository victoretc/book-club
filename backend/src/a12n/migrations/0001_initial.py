import django.db.models.expressions
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies: list = []

    operations = [
        migrations.CreateModel(
            name="EmailVerificationCode",
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
                ("email", models.EmailField(db_index=True, max_length=254)),
                (
                    "code",
                    models.CharField(
                        editable=False, max_length=6
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_used", models.BooleanField(default=False)),
            ],
        ),
        migrations.AddIndex(
            model_name="emailverificationcode",
            index=models.Index(
                fields=["email", "code"],
                name="a12n_emailv_email_6f3ef4_idx",
            ),
        ),
    ]
