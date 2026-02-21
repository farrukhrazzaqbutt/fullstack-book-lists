from rest_framework import serializers

from api.models import Book, BookList


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "year", "author_name"]


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookList
        fields = ["id", "name", "created_at"]
