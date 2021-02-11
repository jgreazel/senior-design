import { Component, EventEmitter, Input, Output } from '@angular/core';
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
    color: null,
    text: null,
    riskIndex: null,
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
      this.data.text = this._selectedNode.data.text;
      this.data.riskIndex = this._selectedNode.data.riskIndex;
    } else {
      this._selectedNode = null;
      this.data.text = null;
      this.data.riskIndex = null;
    }
  }

  constructor() { }

  public onCommitForm() {
    this.onFormChange.emit(this.data);
  }

}
