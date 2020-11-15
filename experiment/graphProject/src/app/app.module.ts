import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { GojsAngularModule } from 'gojs-angular';
import { AppComponent } from './app.component';

import { InspectorComponent } from './inspector/inspector.component';


@NgModule({
  declarations: [
    AppComponent,
    InspectorComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    GojsAngularModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
