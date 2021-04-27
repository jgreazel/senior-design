import { Component, Input, Output, EventEmitter } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'diagram-form',
  templateUrl: './diagram-form.component.html',
  styleUrls: ['./diagram-form.component.css']
})
export class DiagramFormComponent {

  constructor(private fb: FormBuilder) {
  }

  validateForm!: FormGroup;

  acceptableRiskThreshold: number = 0;
  defenseBudget: number = 0;

  @Input()
  public isDefense: boolean;

  @Output()
  public onFormChange: EventEmitter<any> = new EventEmitter<any>();

  ngOnInit(): void {
    this.validateForm = this.fb.group({
      acceptableRiskThreshold: [this.acceptableRiskThreshold, [Validators.required]],
      defenseBudget: [this.defenseBudget, [Validators.required]]
    });
  }

  submitForm(): void {
    this.onFormChange.emit({ acceptableRiskThreshold: this.validateForm.controls.acceptableRiskThreshold.value, 
      defenseBudget: this.validateForm.controls.defenseBudget.value });
  }
}
