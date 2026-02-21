import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../api.service';
import { StoreService } from '../store.service';

@Component({
  standalone: true,
  selector: 'app-books-page',
  imports: [CommonModule],
  template: `
    <h2>All Books</h2>
    <table>
      <thead>
        <tr><th>Title</th><th>Year</th><th>Author</th></tr>
      </thead>
      <tbody>
        @for (b of store.books(); track b.id) {
          <tr>
            <td>{{ b.title }}</td>
            <td>{{ b.year }}</td>
            <td>{{ b.author_name }}</td>
          </tr>
        }
      </tbody>
    </table>
  `,
  styles: [`
    table { width: 100%; border-collapse: collapse; }
    th, td { border-bottom: 1px solid #ddd; padding: 8px; text-align: left; }
  `],
})
export class BooksPageComponent implements OnInit {
  private api = inject(ApiService);
  store = inject(StoreService);

  ngOnInit() {
    this.api.getBooks().subscribe((books) => this.store.books.set(books));
  }
}