import { Component, ViewEncapsulation, AfterViewInit, ChangeDetectorRef, ViewChild } from '@angular/core';
import * as go from 'gojs';
import { DiagramCanvasComponent } from './diagram-canvas/diagram-canvas.component';
import * as _ from 'lodash';
import { ApiService } from './api-handler/api.service';
import { HttpClient } from '@angular/common/http';
import { FileSaverService } from 'ngx-filesaver';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class AppComponent implements AfterViewInit {
  @ViewChild(DiagramCanvasComponent) diagramCanvasComponent: DiagramCanvasComponent;

  public selectedEngine = 'attackTree';
  public selectedNode: go.Node | null = null;
  public observedDiagram = null;
  public acceptableRiskThreshold = 0;
  public defenseBudget = 0;
  public resultsToShow = false;
  public ourData = null;

  constructor(
    private cdr: ChangeDetectorRef,
    private apiService: ApiService,
    private httpClient: HttpClient,
    private fileSaverService: FileSaverService
  ) { }

  /**
   * Called when 'Analyze' button is clicked.
   * Triggers the analyzeData() function in apiService
   * 
   * todo: make asynchronous and show loading spinner before results div
   */
  analyzeData() {
    if (this.validateData()) { // data has been validated
      this.apiService.analyzeData(this.selectedEngine,
        this.acceptableRiskThreshold,
        this.defenseBudget,
        this.diagramCanvasComponent.diagramNodeData,
        this.diagramCanvasComponent.diagramLinkData)
        .subscribe(data => {
          //do something meaningful with data here once connected to BE
          console.log(data);
          this.ourData = data;
          this.resultsToShow = true;
        })
    }
  }

  clickEngineSelect() {
    this.resultsToShow = false;
    console.log(this.resultsToShow)
  }

  /**
   * On initialization this component finds the diagram component and attaches a listener.
   * This listener is triggered when a different diagram node is selected; it then sets that node to selectedNode for the inspectors.
   */
  public ngAfterViewInit() {
    if (this.observedDiagram) return;
    this.observedDiagram = this.diagramCanvasComponent.myDiagramComponent.diagram;
    this.cdr.detectChanges(); // IMPORTANT: without this, Angular will throw ExpressionChangedAfterItHasBeenCheckedError (dev mode only)
    const appComp: AppComponent = this;
    // listener for inspector
    this.diagramCanvasComponent.myDiagramComponent.diagram.addDiagramListener('ChangedSelection', function (e) {
      if (e.diagram.selection.count === 0) {
        appComp.selectedNode = null;
      }
      const node = e.diagram.selection.first();
      if (node instanceof go.Node) {
        appComp.selectedNode = node;
      } else {
        appComp.selectedNode = null;
      }
    });
  }

  /**
   * Sets graph variables from the form
   * @param graphData 
   */
  public handleGraphFormChange(graphData) {
    this.acceptableRiskThreshold = graphData.acceptableRiskThreshold;
    this.defenseBudget = graphData.defenseBudget;
  }

  /**
   * Sets node variables from the form
   * @param newNodeData 
   */
  public handleInspectorChange(newNodeData) {
    const key = newNodeData.key;
    // find the entry in nodeDataArray with this key, replace it with newNodeData
    let index = null;
    for (let i = 0; i < this.diagramCanvasComponent.diagramNodeData.length; i++) {
      const entry = this.diagramCanvasComponent.diagramNodeData[i];
      if (entry.key && entry.key === key) {
        index = i;
      }
    }

    if (index >= 0) {
      // here, we set skipsDiagramUpdate to false, since GoJS does not yet have this update
      this.diagramCanvasComponent.skipsDiagramUpdate = false;
      this.diagramCanvasComponent.diagramNodeData[index] = _.cloneDeep(newNodeData);
    }
  }

  /**
   * 
   * @returns true if tree was validated correctly, false otherwise. 
   */
  validateData() {
    let nodes = this.diagramCanvasComponent.diagramNodeData;
    let links = this.diagramCanvasComponent.diagramLinkData;
    if (this.selectedEngine === 'attackTree') {
      return this.validateAT();
    } else {
      return this.validateADT();
    }
  }

  /**
   * Validate properties of an Attack Tree
   * @returns 
   */
  validateAT() {
    let nodes = this.diagramCanvasComponent.diagramNodeData;
    let links = this.diagramCanvasComponent.diagramLinkData;
    let nodeCount = 0, linkCount = 0, safeCount = 0, rootCount = 0;
    let alertString = "";
    let safePathFound = false;
    for (let i = 0; i < nodes.length; i++) {
      nodeCount++;
      if (nodes[i].key.includes("SAFE")) {
        safeCount++;
        safePathFound = true;
      }
      if (nodes[i].key.includes("ROOT")) {
        rootCount++;
      }
      if (nodes[i].key.includes("DEFENSE")) {
        alertString += "Attack tree cannot contain defense nodes.\n";
      }
    }
    for (let i = 0; i < links.length; i++) {
      linkCount++;
      if (links[i].to.includes("SAFE") && !links[i].from.includes("ROOT")) {
        alertString += "Safe path must be the child of the ROOT node.\n";
      }
    }

    //Nodes should equal edges + 1
    if (linkCount != nodeCount - 1) {
      alertString += "Not a valid tree.\n";
    }

    if (safePathFound == false) {
      alertString += "Must include a safe path.\n";
    }

    if (safeCount > 1) {
      alertString += "The tree must contain only one safe path.\n";
    }

    if (rootCount > 1) {
      alertString += "Tree may only include one root node.\n";
    }

    if (alertString === "") {
      return true;
    } else {
      alert(alertString);
      return false;
    }
  }

  /**
   * Vaildate properties of Attack Defense Tree and Game Theory Tree
   * @returns true if validated, false if not
   */
  validateADT() {
    let nodes = this.diagramCanvasComponent.diagramNodeData;
    let links = this.diagramCanvasComponent.diagramLinkData;
    let nodeCount = 0, linkCount = 0, safeCount = 0, defenseCount = 0, leafCount = 0, rootCount = 0;;
    let alertString = "";
    let safePathFound = false, safePathFromRoot = true, defenseFromLeaf = true;
    for (let i = 0; i < nodes.length; i++) {
      nodeCount++;
      if (nodes[i].key.includes("SAFE")) {
        safeCount++;
        safePathFound = true;
      }
      if (nodes[i].key.includes("LEAF")) {
        leafCount++;
      }
      if (nodes[i].key.includes("DEFENSE")) {
        defenseCount++;
      }
      if (nodes[i].key.includes("ROOT")) {
        rootCount++;
      }
    }
    for (let i = 0; i < links.length; i++) {
      linkCount++;

      if (links[i].to.includes("SAFE") && !links[i].from.includes("ROOT")) {
        safePathFromRoot = false;
      }

      //to defense and not from leaf
      if (links[i].to.includes("DEFENSE") && !links[i].from.includes("LEAF")) {
        defenseFromLeaf = false;
      }
    }

    //Nodes should equal edges + 1
    if (linkCount != nodeCount - 1) {
      alertString += "Not a valid tree.\n";
    }

    if (safePathFound == false) {
      alertString += "Must include a safe path.\n";
    }

    if (safeCount > 1) {
      alertString += "The tree must contain only one safe path.\n";
    }

    if (leafCount != defenseCount) {
      alertString += "Must have one defense node for each leaf node.\n"
    }

    if (rootCount > 1) {
      alertString += "Tree may only include one root node.\n";
    }

    if (safePathFromRoot == false) {
      alertString += "Safe path must be the child of the ROOT node.\n";
    }

    if (defenseFromLeaf == false) {
      alertString += "Defense node must stem from a leaf node.\n";
    }

    if (alertString === "") {
      return true;
    } else {
      alert(alertString);
      return false;
    }
  }

  /**
   * Triggered when 'Save' button is clicked.
   * Saves a json file of the diagram
   */
  onDown(type: string, fromRemote: boolean) {
    let text: string;
    const options = {
      autoBom: false,
    };
    const fileName = `save.${type}`;
    if (fromRemote) {
      this.httpClient.get(`assets/files/demo.${type}`, {
        observe: 'response',
        responseType: 'blob'
      }).subscribe(res => {
        this.fileSaverService.save(res.body, fileName);
      });
      return;
    }
    text = "";
    text += "{\n\"nodes\": " + JSON.stringify(this.diagramCanvasComponent.diagramNodeData) + ",\n";
    text += "\"links\": " + JSON.stringify(this.diagramCanvasComponent.diagramLinkData) + "\n}";
    const fileType = this.fileSaverService.genType(fileName);
    const txtBlob = new Blob([text], { type: fileType });
    this.fileSaverService.save(txtBlob, fileName, null, options);
  }
}