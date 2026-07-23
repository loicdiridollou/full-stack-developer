import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { waitForAsync, ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { IonicModule } from '@ionic/angular';

import { DrinkMenuPage } from './drink-menu.page';

describe('DrinkMenuPage', () => {
  let component: DrinkMenuPage;
  let fixture: ComponentFixture<DrinkMenuPage>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ DrinkMenuPage ],
      imports: [ IonicModule.forRoot() ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
      providers: [ provideHttpClient(), provideHttpClientTesting() ],
    })
    .compileComponents();
  }));

  beforeEach(async () => {
    fixture = TestBed.createComponent(DrinkMenuPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
    // Wait for Ionic's lazy-loaded custom elements (e.g. ion-card) to finish
    // upgrading before the test completes, otherwise their async chunk-load
    // callback fires after teardown and surfaces as an unhandled rejection.
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
