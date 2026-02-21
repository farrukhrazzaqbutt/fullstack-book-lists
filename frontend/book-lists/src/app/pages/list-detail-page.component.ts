import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../api.service';
import { StoreService } from '../store.service';

@Component({
  standalone: true,
  selector: 'app-list-detail-page',
  imports: [CommonModule, FormsModule],
  template: `
    <h2>List Details</h2>

    <div>
      <label for="add-book-select">Add book:</label>
      <select id="add-book-select" [(ngModel)]="selectedBookId">
        <option [ngValue]="null">-- choose --</option>
        @for (b of store.books(); track b.id) {
          <option [ngValue]="b.id">
            {{ b.title }} ({{ b.year }}) - {{ b.author_name }}
          </option>
        }
      </select>
      <button (click)="add()">Add</button>
    </div>

    <h3>Books in this list</h3>
    <ul>
      @for (b of store.selectedListBooks(); track b.id) {
        <li>
          {{ b.title }} ({{ b.year }}) - {{ b.author_name }}
          <button (click)="remove(b.id)">Remove</button>
        </li>
      }
    </ul>
  `,
})
export class ListDetailPageComponent implements OnInit {
  private api = inject(ApiService);
  private route = inject(ActivatedRoute);
  store = inject(StoreService);

  listId!: number;
  selectedBookId: number | null = null;

  ngOnInit() {
    this.listId = Number(this.route.snapshot.paramMap.get('id'));

    // Load all books once (for dropdown)
    if (this.store.books().length === 0) {
      this.api.getBooks().subscribe((books) => this.store.books.set(books));
    }

    this.refreshListBooks();
  }

  refreshListBooks() {
    this.api.getBooksInList(this.listId).subscribe((books) => this.store.selectedListBooks.set(books));
  }

  add() {
    if (!this.selectedBookId) return;
    this.api.addBookToList(this.listId, this.selectedBookId).subscribe(() => {
      this.selectedBookId = null;
      this.refreshListBooks();
    });
  }

  remove(bookId: number) {
    this.api.removeBookFromList(this.listId, bookId).subscribe(() => this.refreshListBooks());
  }
}