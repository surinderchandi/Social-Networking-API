# Create a migration file for adding the index
# 0002_auto_intexing.py
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),  # Adjust the dependency based on your migration history
    ]

    operations = [
        migrations.RunSQL(
            "CREATE INDEX user_search_idx ON users_user USING gin(to_tsvector('english', first_name || ' ' || last_name));"
        ),
    ]
