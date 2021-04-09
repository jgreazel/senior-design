import { Component, OnInit } from '@angular/core';
import { NzModalService } from 'ng-zorro-antd/modal';

@Component({
  selector: 'help-button',
  templateUrl: './help-button.component.html',
  styleUrls: ['./help-button.component.css']
})
export class HelpButtonComponent implements OnInit {

  constructor(private modal: NzModalService) { }

  ngOnInit(): void {
  }

  info() {
    this.modal.info({
      nzTitle: 'Getting Started with CySec Analytics',
      nzWidth: 650,
      nzContent: `<h4>Creating your first diagram</h4>
      <p>Drag & drop nodes from the palette to the diagram beginning with the ROOT_NODE.</p>
      <img src="assets/gettingStarted.jpg" width="350">
      <h4>Diagram Structure</h4>
      <p>Diagrams start with a ROOT_NODE and must branch off towards a SAFE_PATH and the beginning of your structured tree.</p>
      <img src="assets/basicTreeStructure.jpg" width="315">
      <h4>Choosing your Analytical Engine</h4>
      <p>CySec Game provides three analytical engines: Attack Tree, Attack-Defense Tree, and Game Theory. Use the engine selector to choose.</p>
      <img src="assets/engineSelector.jpg" width="200">`
    })
  }

}
