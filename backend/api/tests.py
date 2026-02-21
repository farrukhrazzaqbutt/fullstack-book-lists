"""
Unit tests for the book-lists API.
"""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from api.models import Book, BookList, BookListItem
from api.serializers import BookSerializer, BookListSerializer


class BookModelTests(TestCase):
    """Tests for the Book model."""

    def test_str_representation(self):
        book = Book(title="Test Book", year=2000, author_name="Author")
        self.assertEqual(str(book), "Test Book (2000)")

    def test_unique_title(self):
        Book.objects.create(title="Unique", year=2000, author_name="A")
        with self.assertRaises(Exception):
            Book.objects.create(title="Unique", year=2001, author_name="B")


class BookListModelTests(TestCase):
    """Tests for the BookList model."""

    def test_str_representation(self):
        lst = BookList(name="My List")
        lst.save()
        self.assertEqual(str(lst), "My List")

    def test_unique_name(self):
        BookList.objects.create(name="List One")
        with self.assertRaises(Exception):
            BookList.objects.create(name="List One")


class BookListItemModelTests(TestCase):
    """Tests for the BookListItem model (unique book per list)."""

    def setUp(self):
        self.book = Book.objects.create(
            title="Book One", year=2000, author_name="Author"
        )
        self.book_list = BookList.objects.create(name="List One")

    def test_unique_constraint(self):
        BookListItem.objects.create(book_list=self.book_list, book=self.book)
        with self.assertRaises(Exception):
            BookListItem.objects.create(
                book_list=self.book_list, book=self.book
            )


class BookSerializerTests(TestCase):
    """Tests for BookSerializer."""

    def test_serialize_book(self):
        book = Book.objects.create(
            title="Serialized", year=1999, author_name="Writer"
        )
        data = BookSerializer(book).data
        self.assertEqual(data["title"], "Serialized")
        self.assertEqual(data["year"], 1999)
        self.assertEqual(data["author_name"], "Writer")
        self.assertIn("id", data)

    def test_deserialize_valid_data(self):
        data = {
            "title": "New Book",
            "year": 2020,
            "author_name": "New Author",
        }
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class BookListSerializerTests(TestCase):
    """Tests for BookListSerializer."""

    def test_serialize_list(self):
        lst = BookList.objects.create(name="Test List")
        data = BookListSerializer(lst).data
        self.assertEqual(data["name"], "Test List")
        self.assertIn("id", data)
        self.assertIn("created_at", data)


class BookViewSetTests(TestCase):
    """Tests for BookViewSet (GET list, GET detail)."""

    def setUp(self):
        self.client = APIClient()
        self.book = Book.objects.create(
            title="API Book", year=2005, author_name="API Author"
        )

    def test_list_books(self):
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "API Book")

    def test_retrieve_book(self):
        response = self.client.get(f"/api/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "API Book")
        self.assertEqual(response.data["year"], 2005)


class BookListViewSetTests(TestCase):
    """Tests for BookListViewSet (CRUD + list books, add/remove book)."""

    def setUp(self):
        self.client = APIClient()
        self.book1 = Book.objects.create(
            title="Book A", year=2000, author_name="Author A"
        )
        self.book2 = Book.objects.create(
            title="Book B", year=2001, author_name="Author B"
        )

    def test_list_lists(self):
        BookList.objects.create(name="List 1")
        response = self.client.get("/api/lists/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "List 1")

    def test_create_list(self):
        response = self.client.post(
            "/api/lists/", {"name": "New List"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New List")
        self.assertTrue(BookList.objects.filter(name="New List").exists())

    def test_retrieve_list(self):
        lst = BookList.objects.create(name="Retrieve Me")
        response = self.client.get(f"/api/lists/{lst.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Retrieve Me")

    def test_delete_list(self):
        lst = BookList.objects.create(name="To Delete")
        response = self.client.delete(f"/api/lists/{lst.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BookList.objects.filter(id=lst.id).exists())

    def test_get_books_in_list_empty(self):
        lst = BookList.objects.create(name="Empty List")
        response = self.client.get(f"/api/lists/{lst.id}/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_books_in_list_with_books(self):
        lst = BookList.objects.create(name="Filled List")
        BookListItem.objects.create(book_list=lst, book=self.book1)
        response = self.client.get(f"/api/lists/{lst.id}/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Book A")

    def test_add_book_to_list(self):
        lst = BookList.objects.create(name="Add List")
        response = self.client.post(
            f"/api/lists/{lst.id}/books/",
            {"book_id": self.book1.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["detail"], "added")
        self.assertTrue(
            BookListItem.objects.filter(
                book_list=lst, book=self.book1
            ).exists()
        )

    def test_add_book_to_list_missing_book_id(self):
        lst = BookList.objects.create(name="Bad Add")
        response = self.client.post(
            f"/api/lists/{lst.id}/books/", {}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("book_id", response.data["detail"])

    def test_add_book_to_list_invalid_book_id(self):
        lst = BookList.objects.create(name="Invalid")
        response = self.client.post(
            f"/api/lists/{lst.id}/books/",
            {"book_id": 99999},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_book_idempotent(self):
        lst = BookList.objects.create(name="Idempotent")
        self.client.post(
            f"/api/lists/{lst.id}/books/",
            {"book_id": self.book1.id},
            format="json",
        )
        response = self.client.post(
            f"/api/lists/{lst.id}/books/",
            {"book_id": self.book1.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BookListItem.objects.filter(book_list=lst).count(), 1)

    def test_remove_book_from_list(self):
        lst = BookList.objects.create(name="Remove List")
        BookListItem.objects.create(book_list=lst, book=self.book1)
        response = self.client.delete(
            f"/api/lists/{lst.id}/books/{self.book1.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            BookListItem.objects.filter(
                book_list=lst, book=self.book1
            ).exists()
        )

    def test_remove_book_from_list_not_in_list(self):
        lst = BookList.objects.create(name="No Book")
        response = self.client.delete(
            f"/api/lists/{lst.id}/books/{self.book1.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
