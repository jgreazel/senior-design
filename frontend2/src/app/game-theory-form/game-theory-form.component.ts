import { Component, Input, EventEmitter, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import * as go from 'gojs';

@Component({
  selector: 'game-theory-form',
  templateUrl: './game-theory-form.component.html',
  styleUrls: ['./game-theory-form.component.css']
})
export class GameTheoryFormComponent {

  constructor(private fb: FormBuilder) { }

  _selectedNode: go.Node;
  selectedIsLeaf: boolean;
  validateForm!: FormGroup;

  probability: number;
  label: string;
  impact: number;
  cost: number;

  nodeKeys = ["S", "L", "R"];

  @Input()
  get selectedNode() {
    return this._selectedNode;
  }
  set selectedNode(node: go.Node) {
    if (node && (this.nodeKeys.includes(node.key[0]))) {
      this._selectedNode = node;
      this.selectedIsLeaf = (node.key[0] !== "R");
      this.probability = this._selectedNode.data.probability;
      this.label = this._selectedNode.data.text;
      this.impact = this._selectedNode.data.impact;
      this.cost = this._selectedNode.data.cost;
    } else {
      this._selectedNode = null;
      this.probability = null;
      this.label = null;
      this.impact = null;
      this.cost = null;
    }
  }

  @Output()
  public onFormChange: EventEmitter<any> = new EventEmitter<any>();

  ngOnChanges(): void {
    this.validateForm = this.fb.group({
      probability: [this.probability, [Validators.required]],
      label: [this.label, [Validators.required]],
      impact: [this.impact, [Validators.required]],
      cost: [this.cost, [Validators.required]]
    });
  }

  submitForm(): void {
    for (const i in this.validateForm.controls) {
      this.validateForm.controls[i].markAsDirty();
      this.validateForm.controls[i].updateValueAndValidity();
    }
    const data = this.selectedIsLeaf ? {
        ...this.selectedNode.data,
        probability: this.validateForm.controls.probability.value,
        cost: this.validateForm.controls.cost.value,
        text: this.validateForm.controls.label.value
      } :
      {
        ...this.selectedNode.data,
        impact: this.validateForm.controls.impact.value,
        text: this.validateForm.controls.label.value
      };
    console.log(data)
    this.onFormChange.emit(data)
  }
}
