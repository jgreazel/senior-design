
import { Component, EventEmitter, Inject, Input, Output } from '@angular/core';
import * as go from 'gojs';


@Component({
  selector: 'app-inspector',
  templateUrl: './inspector.component.html',
  styleUrls: ['./inspector.component.css']
})
export class InspectorComponent {

  public _selectedNode: go.Node;
  public data = {
    key: null,
    text: null,
    probability: null,
  };

  @Input()
  public model: go.Model;

  @Output()
  public onFormChange: EventEmitter<any> = new EventEmitter<any>();

  @Input()
  get selectedNode() { return this._selectedNode; }
  set selectedNode(node: go.Node) {
    if (node) {
      this._selectedNode = node;
      this.data.key = this._selectedNode.data.key;
      this.data.probability = this._selectedNode.data.probability;
      this.data.text = this._selectedNode.data.text;
    } else {
      this._selectedNode = null;
      this.data.key = null;
      this.data.probability = null;
      this.data.text = null;
    }
  }

  constructor() { }

  public onCommitForm() {
    this.onFormChange.emit(this.data);
  }

}

