from django.core.management.base import BaseCommand
from shipping.models import Product, Box

class Command(BaseCommand):
    help = "Create demo records without overwriting existing records."
    def handle(self, *args, **options):
        for name, dims, weight in [("Book", (200, 140, 30), 400), ("Mug carton", (100, 100, 120), 350), ("T-shirt", (220, 180, 30), 200)]:
            Product.objects.get_or_create(name=name, defaults=dict(zip(("length_mm", "width_mm", "height_mm", "weight_g"), (*dims, weight))))
        for name, dims, weight, cost in [("Small", (220, 160, 80), 1000, "15.00"), ("Medium", (300, 240, 180), 3000, "25.00"), ("Large", (400, 300, 250), 5000, "40.00")]:
            Box.objects.get_or_create(name=name, defaults=dict(zip(("length_mm", "width_mm", "height_mm", "max_weight_g", "cost"), (*dims, weight, cost))))
        self.stdout.write(self.style.SUCCESS("Demo catalog ready."))
