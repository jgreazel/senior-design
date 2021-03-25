import { Component, Input, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import * as go from 'gojs';

@Component({
  selector: 'atk-tree-form',
  templateUrl: './atk-tree-form.component.html',
  styleUrls: ['./atk-tree-form.component.css']
})
export class AtkTreeFormComponent implements OnInit {

  constructor(private fb: FormBuilder) { }

  _selectedNode: go.Node;
  validateForm!: FormGroup;

  @Input()
  get selectedNode(){
    return this._selectedNode;
  }

  ngOnInit(): void {
    this.validateForm = this.fb.group({
      probability: [null, [Validators.required]]
    });
  }

  submitForm(): void {
    for (const i in this.validateForm.controls) {
      this.validateForm.controls[i].markAsDirty();
      this.validateForm.controls[i].updateValueAndValidity();
    }
  }

  

}
