import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { GojsAngularModule } from 'gojs-angular';

import { AppComponent } from './app.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NZ_I18N } from 'ng-zorro-antd/i18n';
import { en_US } from 'ng-zorro-antd/i18n';
import { registerLocaleData } from '@angular/common';
import en from '@angular/common/locales/en';
import { FileSaverModule } from 'ngx-filesaver';


import { NzGridModule } from 'ng-zorro-antd/grid';
import { NzButtonModule } from 'ng-zorro-antd/button';
import { NzIconModule } from 'ng-zorro-antd/icon';
import { IconDefinition } from '@ant-design/icons-angular';
import { SyncOutline, DeleteOutline, SaveOutline, UploadOutline, InfoCircleTwoTone, ExclamationOutline } from '@ant-design/icons-angular/icons';
import { NzSelectModule } from 'ng-zorro-antd/select';
import { NzFormModule } from 'ng-zorro-antd/form';
import { NzInputModule } from 'ng-zorro-antd/input';
import { NzInputNumberModule } from 'ng-zorro-antd/input-number';
import { NzUploadModule } from 'ng-zorro-antd/upload';
import { NzCollapseModule } from 'ng-zorro-antd/collapse';
import { NzListModule } from 'ng-zorro-antd/list';
import { NzToolTipModule } from 'ng-zorro-antd/tooltip';
import { NzModalModule } from 'ng-zorro-antd/modal';

import { AtkTreePaletteComponent } from './atk-tree-palette/atk-tree-palette.component';
import { AtkDefTreePaletteComponent } from './atk-def-tree-palette/atk-def-tree-palette.component';
import { DiagramCanvasComponent } from './diagram-canvas/diagram-canvas.component';
import { AtkTreeFormComponent } from './atk-tree-form/atk-tree-form.component';
import { AtkDefTreeFormComponent } from './atk-def-tree-form/atk-def-tree-form.component';
import { DiagramFormComponent } from './diagram-form/diagram-form.component';
import { DataVisualizationComponent } from './data-visualization/data-visualization.component';
import { GameTheoryFormComponent } from './game-theory-form/game-theory-form.component';
import { HelpButtonComponent } from './help-button/help-button.component';
import { AttackTreeOutputComponent } from './attack-tree-output/attack-tree-output.component';

registerLocaleData(en);

const icons: IconDefinition[] = [SyncOutline, DeleteOutline, SaveOutline, UploadOutline, InfoCircleTwoTone, ExclamationOutline]

@NgModule({
  declarations: [
    AppComponent,
    AtkTreePaletteComponent,
    AtkDefTreePaletteComponent,
    DiagramCanvasComponent,
    AtkTreeFormComponent,
    AtkDefTreeFormComponent,
    DiagramFormComponent,
    DataVisualizationComponent,
    GameTheoryFormComponent,
    HelpButtonComponent,
    AttackTreeOutputComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    FileSaverModule,
    GojsAngularModule,
    NzGridModule,
    NzButtonModule,
    NzIconModule.forRoot(icons),
    NzSelectModule,
    NzFormModule,
    NzInputModule,
    NzInputNumberModule,
    NzUploadModule,
    NzCollapseModule,
    NzListModule,
    NzToolTipModule,
    NzModalModule
  ],
  providers: [{ provide: NZ_I18N, useValue: en_US }],
  bootstrap: [AppComponent]
})
export class AppModule { }
