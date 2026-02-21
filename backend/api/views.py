from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Book, BookList, BookListItem
from api.serializers import BookListSerializer, BookSerializer


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all().order_by("title")
    serializer_class = BookSerializer


class BookListViewSet(viewsets.ModelViewSet):
    queryset = BookList.objects.all().order_by("-created_at")
    serializer_class = BookListSerializer

    @action(detail=True, methods=["get", "post"], url_path="books")
    def books(self, request, pk=None):
        """
        GET  /api/lists/{id}/books/           -> list books in a list
        POST /api/lists/{id}/books/ body: { "book_id": number } -> add book
        """
        book_list = self.get_object()

        if request.method == "GET":
            books = Book.objects.filter(list_items__book_list=book_list).order_by("title")
            return Response(BookSerializer(books, many=True).data)

        # POST
        book_id = request.data.get("book_id")
        if not book_id:
            return Response({"detail": "book_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        book = get_object_or_404(Book, pk=book_id)
        BookListItem.objects.get_or_create(book_list=book_list, book=book)
        return Response({"detail": "added"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"], url_path=r"books/(?P<book_id>\d+)")
    def remove_book(self, request, pk=None, book_id=None):
        """
        DELETE /api/lists/{id}/books/{book_id}/ -> remove book from list
        """
        book_list = self.get_object()
        item = BookListItem.objects.filter(book_list=book_list, book_id=book_id).first()
        if not item:
            return Response({"detail": "not found"}, status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
