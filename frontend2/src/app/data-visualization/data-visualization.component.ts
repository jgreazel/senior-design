import { Component, OnInit } from '@angular/core';




@Component({
  selector: 'data-visualization',
  templateUrl: './data-visualization.component.html',
  styleUrls: ['./data-visualization.component.css']
})
export class DataVisualizationComponent implements OnInit {

  public dummyData = {
    "cost": 400,
    "defendedAttacks": ["LEAF", "LEAF1", "LEAF2"],
    "attackScenarios": [
      {
      "risk": 45,
      "predefenseRisk": 45,
      "attacks": ["LEAF", "LEAF1", "LEAF2", "LEAF3","LEAF2", "LEAF3", "LEAF2", "LEAF3"]
      },
      {
      "risk": 40,
      "predefenseRisk": 45,
      "attacks": ["LEAF", "LEAF1", "LEAF2"]
      },
      {
      "risk": 35,
      "predefenseRisk": 45,
      "attacks": ["LEAF", "LEAF1", "LEAF2"]
      }
    ]
  }

  constructor() { }

  ngOnInit(): void {
    console.log(this.dummyData);
  }

}
