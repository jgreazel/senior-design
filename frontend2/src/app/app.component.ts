import { Component, ViewEncapsulation, AfterViewInit, ChangeDetectorRef, ViewChild } from '@angular/core';
import * as go from 'gojs';
import { DiagramComponent } from 'gojs-angular';
import { DiagramCanvasComponent } from './diagram-canvas/diagram-canvas.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class AppComponent implements AfterViewInit{
  @ViewChild(DiagramCanvasComponent) myDiagramComponent: DiagramComponent;
  
  selectedEngine = 'attackTree';
  selectedNode: go.Node | null = null;
  observedDiagram = null;

  constructor(
    private cdr: ChangeDetectorRef
    // private apiService: ApiService,
    // private httpClient: HttpClient,
    // private fileSaverService: FileSaverService
    ) { }

    public ngAfterViewInit() {
      
      console.log('diagram', this.myDiagramComponent);
      if (this.observedDiagram) return;
      this.observedDiagram = this.myDiagramComponent.diagram;
      this.cdr.detectChanges(); // IMPORTANT: without this, Angular will throw ExpressionChangedAfterItHasBeenCheckedError (dev mode only)
      const appComp: AppComponent = this;
      // listener for inspector
      this.myDiagramComponent.diagram.addDiagramListener('ChangedSelection', function (e) {
        console.log('this going?')
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
    } // end ngAfterViewInit
}
