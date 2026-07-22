import { Component, OnInit, Input, ChangeDetectionStrategy } from '@angular/core';
import { Drink, DrinksService } from 'src/app/services/drinks.service';
import { ModalController } from '@ionic/angular';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-drink-form',
  standalone: false,
  templateUrl: './drink-form.component.html',
  changeDetection: ChangeDetectionStrategy.Eager,
  styleUrls: ['./drink-form.component.scss'],
})
export class DrinkFormComponent implements OnInit {
  @Input() drink!: Drink;
  @Input() isNew!: boolean;

  constructor(
    public auth: AuthService,
    private modalCtrl: ModalController,
    private drinkService: DrinksService
    ) { }

  ngOnInit() {
    if (this.isNew) {
      this.drink = {
        id: -1,
        title: '',
        recipe: []
      };
      this.addIngredient();
    }
  }

  customTrackBy(index: number): number {
    return index;
  }

  addIngredient(i = 0) {
    this.drink.recipe.splice(i + 1, 0, {name: '', color: 'white', parts: 1});
  }

  removeIngredient(i: number) {
    this.drink.recipe.splice(i, 1);
  }

  closeModal() {
    this.modalCtrl.dismiss();
  }

  saveClicked() {
    this.drinkService.saveDrink(this.drink);
    this.closeModal();
  }

  deleteClicked() {
    this.drinkService.deleteDrink(this.drink);
    this.closeModal();
  }
}
