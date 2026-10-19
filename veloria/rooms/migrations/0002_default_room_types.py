from django.db import migrations

DEFAULT_ROOM_TYPES = [
    ('Deluxe Room', 'Spacious deluxe room'),
    ('Executive Suite', 'Premium executive suite'),
    ('Presidential Suite', 'Top floor presidential suite'),
]


def create_room_types(apps, schema_editor):
    RoomType = apps.get_model('rooms', 'RoomType')
    for name, description in DEFAULT_ROOM_TYPES:
        RoomType.objects.get_or_create(name=name, defaults={'description': description})


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_room_types, migrations.RunPython.noop),
    ]
