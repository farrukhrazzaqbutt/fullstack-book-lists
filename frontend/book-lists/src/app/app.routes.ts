import { Routes } from '@angular/router';
import { BooksPageComponent } from './pages/books-page.component';
import { ListsPageComponent } from './pages/lists-page.component';
import { ListDetailPageComponent } from './pages/list-detail-page.component';


export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'books' },
  { path: 'books', component: BooksPageComponent },
  { path: 'lists', component: ListsPageComponent },
  { path: 'lists/:id', component: ListDetailPageComponent },
];
