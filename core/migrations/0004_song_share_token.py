import uuid
from django.db import migrations, models


def populate_share_tokens(apps, schema_editor):
    Song = apps.get_model('core', 'Song')
    for song in Song.objects.filter(share_token=None):
        song.share_token = uuid.uuid4()
        song.save(update_fields=['share_token'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_song_created_at'),
    ]

    operations = [
        # Step 1: add nullable (so existing rows don't conflict)
        migrations.AddField(
            model_name='song',
            name='share_token',
            field=models.UUIDField(null=True, unique=False),
        ),
        # Step 2: fill existing rows with unique UUIDs
        migrations.RunPython(populate_share_tokens, migrations.RunPython.noop),
        # Step 3: enforce not-null + unique
        migrations.AlterField(
            model_name='song',
            name='share_token',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
