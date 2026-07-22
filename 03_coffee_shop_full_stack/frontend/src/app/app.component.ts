import { Component, ChangeDetectionStrategy } from '@angular/core';

import { Platform } from '@ionic/angular';
import { SplashScreen } from '@capacitor/splash-screen';
import { StatusBar, Style } from '@capacitor/status-bar';
import { AuthService } from './services/auth.service';

@Component({
  selector: 'app-root',
  standalone: false,
  changeDetection: ChangeDetectionStrategy.Eager,
  templateUrl: 'app.component.html'
})
export class AppComponent {
  constructor(
    private auth: AuthService,
    private platform: Platform
  ) {
    this.initializeApp();
  }

  initializeApp() {
    this.platform.ready().then(() => {
      StatusBar.setStyle({ style: Style.Default });
      SplashScreen.hide();

      // Perform required auth actions
      this.auth.load_jwts();
      this.auth.check_token_fragment();
    });
  }
}
