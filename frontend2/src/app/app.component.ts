import { Component, ViewChild, ViewEncapsulation } from '@angular/core';
import { DataSyncService, DiagramComponent, PaletteComponent } from 'gojs-angular';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class AppComponent {
  @ViewChild('myPalette', { static: true }) public myPaletteComponent: PaletteComponent;

  selectedEngine = 'attackTree';

}
