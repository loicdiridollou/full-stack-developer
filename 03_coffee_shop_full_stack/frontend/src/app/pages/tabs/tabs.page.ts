import { Component, ChangeDetectionStrategy } from '@angular/core';

@Component({
  selector: 'app-tabs',
  standalone: false,
  templateUrl: 'tabs.page.html',
  changeDetection: ChangeDetectionStrategy.Eager,
  styleUrls: ['tabs.page.scss']
})
export class TabsPage {}
