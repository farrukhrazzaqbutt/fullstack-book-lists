from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    year = models.PositiveIntegerField()
    author_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.title} ({self.year})"


class BookList(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class BookListItem(models.Model):
    book_list = models.ForeignKey(BookList, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="list_items")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["book_list", "book"], name="uniq_book_per_list"),
        ]

    def __str__(self) -> str:
        return f"{self.book_list} -> {self.book}"
