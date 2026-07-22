import { Component, ChangeDetectionStrategy } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-user-page',
  standalone: false,
  templateUrl: './user-page.page.html',
  changeDetection: ChangeDetectionStrategy.Eager,
  styleUrls: ['./user-page.page.scss'],
})
export class UserPagePage {
  loginURL: string;

  constructor(public auth: AuthService) {
    this.loginURL = auth.build_login_link('/tabs/user-page');
  }
}
