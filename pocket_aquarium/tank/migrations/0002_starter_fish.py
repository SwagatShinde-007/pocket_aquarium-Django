from django.db import migrations


def add_starters(apps, schema_editor):
    Fish = apps.get_model("tank", "Fish")
    if Fish.objects.exists():
        return
    Fish.objects.bulk_create([
        Fish(name="Coral", color="#ff6f59", size=120, speed=17, depth=30),
        Fish(name="Bubbles", color="#ffd166", size=90, speed=11, depth=55),
        Fish(name="Nemo-ish", color="#7fe3d0", size=150, speed=24, depth=72),
    ])


def remove_starters(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("tank", "0001_initial")]
    operations = [migrations.RunPython(add_starters, remove_starters)]
