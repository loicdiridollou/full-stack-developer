import { Component, Input, ChangeDetectionStrategy } from '@angular/core';
import { Drink } from 'src/app/services/drinks.service';

@Component({
  selector: 'app-drink-graphic',
  standalone: false,
  templateUrl: './drink-graphic.component.html',
  changeDetection: ChangeDetectionStrategy.Eager,
  styleUrls: ['./drink-graphic.component.scss'],
})
export class DrinkGraphicComponent {
  @Input() drink!: Drink;
}
