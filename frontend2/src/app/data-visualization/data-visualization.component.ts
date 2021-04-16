import { Component, Input, OnInit, OnChanges } from '@angular/core';
// TODO: Rename - this is attack defense 

@Component({
  selector: 'data-visualization',
  templateUrl: './data-visualization.component.html',
  styleUrls: ['./data-visualization.component.css']
})
export class DataVisualizationComponent implements OnInit, OnChanges {
  @Input() data:any;
  public ourData:any;

  constructor() { }

  ngOnInit(): void {
    console.log(this.data);
    this.ourData = JSON.parse(this.data);
    this.ourData.attackScenarios.forEach(element => (element as string).slice(0,5));
    console.log("this one " + this.ourData);
  }

  ngOnChanges() {
    this.ourData = JSON.parse(this.data);
    this.ourData.attackScenarios.forEach(element => (element as string).slice(0,5));
    console.log("--onchages--")
    console.log(this.ourData + " \nOURS " + this.ourData.cost)
  }

}