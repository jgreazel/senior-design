import { Component, Input, OnInit, OnChanges } from '@angular/core';

@Component({
  selector: 'attack-tree-output',
  templateUrl: './attack-tree-output.component.html',
  styleUrls: ['./attack-tree-output.component.css']
})
export class AttackTreeOutputComponent implements OnInit, OnChanges {
  @Input() data:any;
  public ourData:any;
  constructor() { }

  ngOnInit(): void {
    this.ourData = JSON.parse(this.data);
  }

  ngOnChanges() {
    this.ourData = JSON.parse(this.data);
  }

}
