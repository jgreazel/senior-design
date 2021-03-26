import { Component, ViewEncapsulation, AfterViewInit, ChangeDetectorRef, ViewChild } from '@angular/core';
import * as go from 'gojs';
import { DiagramCanvasComponent } from './diagram-canvas/diagram-canvas.component';
import * as _ from 'lodash';

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

  constructor(
    private cdr: ChangeDetectorRef
    // private apiService: ApiService,
    // private httpClient: HttpClient,
    // private fileSaverService: FileSaverService
  ) { }

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
}
