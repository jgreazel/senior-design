
import { Component, EventEmitter, Inject, Input, Output } from '@angular/core';
import * as go from 'gojs';


@Component({
  selector: 'app-inspector',
  templateUrl: './inspector.component.html',
  styleUrls: ['./inspector.component.css']
})
export class InspectorComponent {

  public _selectedNode: go.Node;
  public _isSafePath: boolean;
  public data = {
    key: null,
    text: null,
    probability: null,
    defenseCost: null
  };

  @Input()
  public model: go.Model;

  @Output()
  public onFormChange: EventEmitter<any> = new EventEmitter<any>();

  @Input()
  get selectedNode() {
    return this._selectedNode;
  }
  set selectedNode(node: go.Node) {
    if (node && (node.key[0] === "S" || node.key[0] === "L")) {
      this._selectedNode = node;
      this._isSafePath = (node.key[0] === "L");
      this.data.key = this._selectedNode.data.key;
      this.data.probability = this._selectedNode.data.probability;
      this.data.defenseCost = this._selectedNode.data.defenseCost;
      this.data.text = this._selectedNode.data.text;
    } else {
      this._selectedNode = null;
      this._isSafePath = false;
      this.data.key = null;
      this.data.probability = null;
      this.data.defenseCost = null;
      this.data.text = null;
    }
  }

  constructor() { }

  public onCommitForm() {
    this.onFormChange.emit(this.data);
  }

}

