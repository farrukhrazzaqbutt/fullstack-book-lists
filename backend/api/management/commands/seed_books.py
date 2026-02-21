from django.core.management.base import BaseCommand

from api.models import Book


class Command(BaseCommand):
    help = "Seed initial books for the technical test"

    def handle(self, *args, **options):
        books = [
            {"title": "Dune", "year": 1965, "author_name": "Frank Herbert"},
            {"title": "Ender's Game", "year": 1985, "author_name": "Orson Scott Card"},
            {"title": "1984", "year": 1949, "author_name": "George Orwell"},
            {"title": "Fahrenheit 451", "year": 1953, "author_name": "Ray Bradbury"},
            {"title": "Brave New World", "year": 1932, "author_name": "Aldous Huxley"},
        ]

        created_count = 0
        for b in books:
            _, created = Book.objects.get_or_create(title=b["title"], defaults=b)
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Seed complete. Created {created_count} new books."))
