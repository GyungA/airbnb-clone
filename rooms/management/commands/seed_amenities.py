from django.core.management.base import BaseCommand
from rooms import models as room_models

class Command(BaseCommand):
    help = "This command creates amenities"
    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--times",
    #         help="How many times do you want me to tell you that I love you?",
    #     )

    def handle(self, *args, **options):
        amenities = [
            "Kitchen",
            "Heating",
            "Washer",
            "Wifi",
            "Indoor fireplace",
            "Iron",
            "Laptop friendly workspace",
            "Crib",
            "Self check-in",
            "Carbon monoxide detector",
            "Shampoo",
            "Air conditioning",
            "Dryer",
            "Breakfast",
            "Hangers",
            "Hair dryer",
            "TV",
            "High chair",
            "Smoke detector",
            "Private bathroom",
        ]
        
        count = 0
        for item in amenities:
            if not room_models.Amenity.objects.filter(name=item):
                room_models.Amenity.objects.create(name=item)
                count += 1
        self.stdout.write(self.style.SUCCESS(f"{count} amenities created!"))