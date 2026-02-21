import { Injectable, signal } from '@angular/core';
import { Book, BookList } from './models';

@Injectable({ providedIn: 'root' })
export class StoreService {
  books = signal<Book[]>([]);
  lists = signal<BookList[]>([]);
  selectedListBooks = signal<Book[]>([]);
}