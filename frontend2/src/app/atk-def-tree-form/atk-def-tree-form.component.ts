import { Component, Input, EventEmitter, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import * as go from 'gojs';

@Component({
  selector: 'atk-def-tree-form',
  templateUrl: './atk-def-tree-form.component.html',
  styleUrls: ['./atk-def-tree-form.component.css']
})
export class AtkDefTreeFormComponent {

  constructor(private fb: FormBuilder) { }

  _selectedNode: go.Node;
  validateForm!: FormGroup;

  probability: number;
  label: string;
  impact: number;
  defenseCost: number;
  preDefenseProbability: number;
  postDefenseProbability: number;

  nodeKeys = ["S", "L", "R", "D"];

  @Input()
  get selectedNode() {
    return this._selectedNode;
  }
  set selectedNode(node: go.Node) {
    if (node && (this.nodeKeys.includes(node.key[0]))) {
      this._selectedNode = node;
      this.probability = this._selectedNode.data.probability;
      this.label = this._selectedNode.data.text;
      this.impact = this._selectedNode.data.impact;
      this.defenseCost = this._selectedNode.data.defenseCost;
      this.preDefenseProbability = this._selectedNode.data.preDefenseProbability;
      this.postDefenseProbability = this._selectedNode.data.postDefenseProbability;
    } else {
      this._selectedNode = null;
      this.probability = null;
      this.label = null;
      this.impact = null;
      this.defenseCost = null;
      this.preDefenseProbability = null;
      this.postDefenseProbability = null;
    }
  }

  @Output()
  public onFormChange: EventEmitter<any> = new EventEmitter<any>();

  ngOnChanges(): void {
    this.validateForm = this.fb.group({
      probability: [this.probability, [Validators.required]],
      label: [this.label, [Validators.required]],
      impact: [this.impact, [Validators.required]],
      preDefenseProbability: [this.preDefenseProbability, [Validators.required]],
      postDefenseProbability: [this.postDefenseProbability, [Validators.required]],
      defenseCost: [this.defenseCost, [Validators.required]]
    });
  }

  getData =(nodeType: string)=>{
    if(nodeType === "L"){
      return {
        ...this.selectedNode.data,
        preDefenseProbability: this.validateForm.controls.preDefenseProbability.value,
        postDefenseProbability: this.validateForm.controls.postDefenseProbability.value,
        text: this.validateForm.controls.label.value
      }
    }
    if(nodeType === "R"){
      return {
        ...this.selectedNode.data,
        impact: this.validateForm.controls.impact.value,
        text: this.validateForm.controls.label.value
      }
    }
    if(nodeType === "D"){
      return {
        ...this.selectedNode.data,
        defenseCost: this.validateForm.controls.defenseCost.value,
        text: this.validateForm.controls.label.value
      }
    }
    if(nodeType === "S"){
      return {
        ...this.selectedNode.data,
        probability: this.validateForm.controls.probability.value,
        text: this.validateForm.controls.label.value
      }
    }
  }

  submitForm(): void {
    for (const i in this.validateForm.controls) {
      this.validateForm.controls[i].markAsDirty();
      this.validateForm.controls[i].updateValueAndValidity();
    }
    const data = this.getData(this.selectedNode.key[0]);
    
    console.log(data)
    this.onFormChange.emit(data)
  }
}
