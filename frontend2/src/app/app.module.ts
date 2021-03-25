import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { GojsAngularModule } from 'gojs-angular';

import { AppComponent } from './app.component';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NZ_I18N } from 'ng-zorro-antd/i18n';
import { en_US } from 'ng-zorro-antd/i18n';
import { registerLocaleData } from '@angular/common';
import en from '@angular/common/locales/en';

import { NzGridModule } from 'ng-zorro-antd/grid';
import { NzButtonModule } from 'ng-zorro-antd/button';
import { NzSelectModule } from 'ng-zorro-antd/select';

import { AtkTreePaletteComponent } from './atk-tree-palette/atk-tree-palette.component';
import { AtkDefTreePaletteComponent } from './atk-def-tree-palette/atk-def-tree-palette.component';
import { DiagramCanvasComponent } from './diagram-canvas/diagram-canvas.component';

registerLocaleData(en);

@NgModule({
  declarations: [
    AppComponent,
    AtkTreePaletteComponent,
    AtkDefTreePaletteComponent,
    DiagramCanvasComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    GojsAngularModule,
    NzGridModule,
    NzButtonModule,
    NzSelectModule,
  ],
  providers: [{ provide: NZ_I18N, useValue: en_US }],
  bootstrap: [AppComponent]
})
export class AppModule { }
