import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-root',
  imports: [RouterModule],
  template: `
    <nav style="display:flex; gap:12px; margin-bottom:16px;">
      <a routerLink="/books">Books</a>
      <a routerLink="/lists">Lists</a>
    </nav>
    <router-outlet />
  `,
})
export class AppComponent {}