import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { ApiService } from '../api.service';
import { StoreService } from '../store.service';

@Component({
  standalone: true,
  selector: 'app-lists-page',
  imports: [CommonModule, FormsModule, RouterModule],
  template: `
    <h2>Book Lists</h2>

    <form (ngSubmit)="create()">
      <input [(ngModel)]="name" name="name" placeholder="List name" required />
      <button type="submit">Create</button>
    </form>

    <ul>
      @for (l of store.lists(); track l.id) {
        <li>
          <a [routerLink]="['/lists', l.id]">{{ l.name }}</a>
          <button (click)="remove(l.id)">Delete</button>
        </li>
      }
    </ul>
  `,
})
export class ListsPageComponent implements OnInit {
  private api = inject(ApiService);
  store = inject(StoreService);

  name = '';

  ngOnInit() {
    this.refresh();
  }

  refresh() {
    this.api.getLists().subscribe((lists) => this.store.lists.set(lists));
  }

  create() {
    const trimmed = this.name.trim();
    if (!trimmed) return;

    this.api.createList(trimmed).subscribe(() => {
      this.name = '';
      this.refresh();
    });
  }

  remove(listId: number) {
    this.api.deleteList(listId).subscribe(() => this.refresh());
  }
}