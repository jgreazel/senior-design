import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { GojsAngularModule } from 'gojs-angular';
import { AppComponent } from './app.component';
import {MatButtonModule} from '@angular/material/button';
import { InspectorComponent } from './inspector/inspector.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatSliderModule } from '@angular/material/slider';
import {MatListModule} from '@angular/material/list';
import {MatFormFieldModule} from "@angular/material/form-field";
import { MatIconModule} from '@angular/material/icon';
import { FileSaverModule } from 'ngx-filesaver';

@NgModule({
  declarations: [
    AppComponent,
    InspectorComponent
  ],
  imports: [
    BrowserModule,
    MatSliderModule,
    MatButtonModule,
    FormsModule,
    HttpClientModule,
    GojsAngularModule,
    BrowserAnimationsModule,
    MatListModule,
    MatFormFieldModule,
    MatIconModule,
    FileSaverModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
