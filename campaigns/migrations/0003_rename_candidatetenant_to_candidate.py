from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("campaigns", "0002_add_user_to_candidatetenant"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="CandidateTenant",
            new_name="Candidate",
        ),
    ]
