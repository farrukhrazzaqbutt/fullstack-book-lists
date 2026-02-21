import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Book, BookList } from './models';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  private baseUrl = 'http://127.0.0.1:8000/api';

  getBooks() {
    return this.http.get<Book[]>(`${this.baseUrl}/books/`);
  }

  getLists() {
    return this.http.get<BookList[]>(`${this.baseUrl}/lists/`);
  }

  createList(name: string) {
    return this.http.post<BookList>(`${this.baseUrl}/lists/`, { name });
  }

  deleteList(listId: number) {
    return this.http.delete(`${this.baseUrl}/lists/${listId}/`);
  }

  getBooksInList(listId: number) {
    return this.http.get<Book[]>(`${this.baseUrl}/lists/${listId}/books/`);
  }

  addBookToList(listId: number, bookId: number) {
    return this.http.post(`${this.baseUrl}/lists/${listId}/books/`, { book_id: bookId });
  }

  removeBookFromList(listId: number, bookId: number) {
    return this.http.delete(`${this.baseUrl}/lists/${listId}/books/${bookId}/`);
  }
}