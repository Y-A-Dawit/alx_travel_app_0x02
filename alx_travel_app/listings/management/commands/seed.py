# listings/management/commands/seed.py

from django.core.management.base import BaseCommand
from listings.models import Listing
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **kwargs):
        sample_data = [
            {
                'title': 'Cozy Cottage',
                'description': 'A nice place in the woods.',
                'location': 'Seattle',
                'price_per_night': 120.00,
                'is_available': True
            },
            {
                'title': 'Modern Apartment',
                'description': 'Downtown luxury apartment.',
                'location': 'New York',
                'price_per_night': 250.00,
                'is_available': True
            },
            {
                'title': 'Beach House',
                'description': 'Perfect view of the ocean.',
                'location': 'Miami',
                'price_per_night': 300.00,
                'is_available': False
            }
        ]

        for data in sample_data:
            Listing.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded listings!'))
