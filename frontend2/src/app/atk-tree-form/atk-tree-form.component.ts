import { Component, Input, EventEmitter, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import * as go from 'gojs';

@Component({
  selector: 'atk-tree-form',
  templateUrl: './atk-tree-form.component.html',
  styleUrls: ['./atk-tree-form.component.css']
})
export class AtkTreeFormComponent {

  constructor(private fb: FormBuilder) { }

  _selectedNode: go.Node;
  selectedIsLeaf: boolean;
  validateForm!: FormGroup;

  probability: number;
  label: string;
  impact: number;

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
    } else {
      this._selectedNode = null;
      this.probability = null;
      this.label = null;
      this.impact = null;
    }
  }

  @Output()
  public onFormChange: EventEmitter<any> = new EventEmitter<any>();

  ngOnChanges(): void {
    this.validateForm = this.fb.group({
      probability: [this.probability, [Validators.required]],
      label: [this.label, [Validators.required]],
      impact: [this.impact, [Validators.required]]
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
