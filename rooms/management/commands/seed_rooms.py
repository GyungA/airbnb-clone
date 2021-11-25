import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models

class Command(BaseCommand):
    help = "This command creates rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many rooms you want to create"
            )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_type = room_models.RoomType.objects.all()
        seeder.add_entity(room_models.Room, number,
        {
            "name": lambda x: seeder.faker.company(),
            "host": lambda x: random.choice(all_users), 
            "room_type": lambda x: random.choice(room_type),
            "guests": lambda x: random.randint(1, 20),
            "price": lambda x: random.randint(1, 300),
            "beds": lambda x: random.randint(1, 5),
            "bedrooms": lambda x: random.randint(1, 5),
            "baths": lambda x: random.randint(1, 5),
            })
        created_rooms = seeder.execute()
        print(created_rooms.values())
        created_clean = flatten(created_rooms.values())
        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            for i in range(3, random.randint(10, 17)):
                room_models.Photo.objects.create(
                    caption = seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 31)}.webp",
                )
        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))
