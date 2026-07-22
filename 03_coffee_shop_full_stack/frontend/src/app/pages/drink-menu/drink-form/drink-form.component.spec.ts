import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { waitForAsync, ComponentFixture, TestBed } from '@angular/core/testing';
import { ModalController } from '@ionic/angular';

import { DrinkFormComponent } from './drink-form.component';

describe('DrinkFormComponent', () => {
  let component: DrinkFormComponent;
  let fixture: ComponentFixture<DrinkFormComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ DrinkFormComponent ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
      providers: [ ModalController ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DrinkFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
