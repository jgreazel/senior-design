import { Component, OnInit } from '@angular/core';
import { Person } from '../person'

@Component({
  selector: 'app-my-component',
  templateUrl: './my-component.component.html',
  styleUrls: ['./my-component.component.css']
})
export class MyComponentComponent implements OnInit {

  person: Person = {
    id: 1,
    name: 'Joe'
  }

  constructor() { }

  ngOnInit(): void {
  }

}
