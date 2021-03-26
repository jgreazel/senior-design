import { Component, ViewEncapsulation, AfterViewInit, ChangeDetectorRef, ViewChild } from '@angular/core';
import * as go from 'gojs';
import { DiagramCanvasComponent } from './diagram-canvas/diagram-canvas.component';
import * as _ from 'lodash';
import { ApiService } from './api-handler/api.service';
import { HttpClient } from '@angular/common/http';

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

  constructor(
    private cdr: ChangeDetectorRef,
    private apiService: ApiService,
    private httpClient: HttpClient,
    // private fileSaverService: FileSaverService
  ) { }

  /**
   * Called when 'Analyze' button is clicked.
   * Triggers the analyzeData() function in apiService
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
        })
    }
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
  * Returns 
  *  true if data has been successfully validated
  *  false if there is an error in the data
  */
  validateData() {
    let nodes = this.diagramCanvasComponent.diagramNodeData;
    let links = this.diagramCanvasComponent.diagramLinkData;
    let safePathSum: number = 0;
    let alertString: string = ""
    for (let i = 0; i < nodes.length; i++) {
      // if safe path node, add to count
      if (nodes[i].key.includes("SAFE")) {
        safePathSum += 1;
        if (safePathSum > 1) { // If there'smore than one safe path
          alertString += "Only one safe path is allowed.\n";
          break;
        }
      }
    }
    for (let i = 0; i < links.length; i++) {
      // if link to safe node and not from an or node
      if (links[i].to.includes("SAFE") && !links[i].from.includes("ROOT")) {
        alertString += "Safe path must be the child of the ROOT node.\n";
        break;
      }
    }
    // there should always be one more node than links
    if ((nodes.length - 1) != links.length) {
      alertString += "A tree property has been violated.\n"
    }
    if (alertString !== "") {
      alert(alertString);
      return false;
    } else {
      return true;
    }
  }

  // onDown(type: string, fromRemote: boolean) {
  //   const fileName = `save.${type}`;
  //   if (fromRemote) {
  //     this.httpClient.get(`assets/files/demo.${type}`, {
  //       observe: 'response',
  //       responseType: 'blob'
  //     }).subscribe(res => {
  //       this.fileSaverService.save(res.body, fileName);
  //     });
  //     return;
  //   }
  //   this.text = "";
  //   this.text += "{\n\"nodes\": " + JSON.stringify(this.diagramNodeData) + ",\n";
  //   this.text += "\"links\": " + JSON.stringify(this.diagramLinkData) + "\n}";
  //   const fileType = this.fileSaverService.genType(fileName);
  //   const txtBlob = new Blob([this.text], { type: fileType });
  //   this.fileSaverService.save(txtBlob, fileName, null, this.options);
  // }
}
