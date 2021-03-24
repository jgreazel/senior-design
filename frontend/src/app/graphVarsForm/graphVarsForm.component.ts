
import { NumberSymbol } from '@angular/common';
import { NullTemplateVisitor } from '@angular/compiler';
import { Component, EventEmitter, Inject, Input, Output } from '@angular/core';
import * as go from 'gojs';

@Component({
    selector: 'graph-vars-form',
    templateUrl: './graphVarsForm.component.html',
    styleUrls: ['./graphVarsForm.component.css']
  })
  export class graphVarsForm{

    public _isDefense: boolean;
    public data = {
        acceptableRiskThreshold: 0,
        budget: 0
    }

    @Input()
    get isDefense(){
        return this._isDefense;
    }
    set isDefense(flag: boolean){
        if(flag){
            this._isDefense = flag;
            // might not be the right approach
        }
    }

  }