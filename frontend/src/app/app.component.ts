import { ChangeDetectorRef, Component, ViewChild, ViewEncapsulation } from '@angular/core';
import * as go from 'gojs';
import { DataSyncService, DiagramComponent, PaletteComponent } from 'gojs-angular';
import * as _ from 'lodash';
import { ApiService } from './api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class AppComponent {

  @ViewChild('myDiagram', { static: true }) public myDiagramComponent: DiagramComponent;
  @ViewChild('myPalette', { static: true }) public myPaletteComponent: PaletteComponent;


  // TEST POST METHOD
  computeNodeData() {
    let rando = Math.random();
    this.apiService.computeNodeData({ "id": rando, "key": rando, "color": "red" })
      .subscribe(data => {
        console.log(data);
      })
  }

  // TEST GET METHOD
  getNodeData() {
    this.apiService.getNodeData()
      .subscribe(data => {
        console.log('nodes', data);
        this.diagramNodeData = data
        // this.diagramLinkData = null;
      })
  }

  // initialize diagram / templates
  public initDiagram(): go.Diagram {

    //create custom shape for and-gate
    go.Shape.defineFigureGenerator("AndGate", function (shape, w, h) {
      var geo = new go.Geometry();
      var cpOffset = (4 * ((Math.sqrt(2) - 1) / 3)) * .5;
      var fig = new go.PathFigure(0, 0, true);
      geo.add(fig);
      h = 2*h;
      w = 1.5 * w;
      // The gate body
      fig.add(new go.PathSegment(go.PathSegment.Line, .5 * w, 0));
      fig.add(new go.PathSegment(go.PathSegment.Bezier, w, .5 * h, (.5 + cpOffset) * w, 0,
        w, (.5 - cpOffset) * h));
      fig.add(new go.PathSegment(go.PathSegment.Bezier, .5 * w, h, w, (.5 + cpOffset) * h,
        (.5 + cpOffset) * w, h));
      fig.add(new go.PathSegment(go.PathSegment.Line, 0, h).close());

      geo.rotate(270, w/3, h/2)
      geo.spot1 = go.Spot.TopLeft;
      geo.spot2 = go.Spot.BottomRight;
      return geo;
    })

    //create custom shape for or-gate
    go.Shape.defineFigureGenerator("OrGate", function(shape, w, h) {
      var geo = new go.Geometry();
      var radius = .5;
      var cpOffset = (4 * ((Math.sqrt(2) - 1) / 3)) * radius;
      var centerx = 0;
      var centery = .5;
      var fig = new go.PathFigure(0, 0, true);
      geo.add(fig);
      h=2*h;
      w=1.5*w;
    
      fig.add(new go.PathSegment(go.PathSegment.Bezier, w, .5 * h, (centerx + cpOffset + cpOffset) * w, (centery - radius) * h,
        .8 * w, (centery - cpOffset) * h));
      fig.add(new go.PathSegment(go.PathSegment.Bezier, 0, h, .8 * w, (centery + cpOffset) * h,
        (centerx + cpOffset + cpOffset) * w, (centery + radius) * h));
      fig.add(new go.PathSegment(go.PathSegment.Bezier, 0, 0, .25 * w, .75 * h, .25 * w, .25 * h).close());
      geo.rotate(270, w/3, h/2)
      geo.spot1 = new go.Spot(.2, .25);
      geo.spot2 = new go.Spot(.75, .75);
      return geo;
    });

    const $ = go.GraphObject.make;
    const dia = $(go.Diagram, {
      initialAutoScale: go.Diagram.UniformToFill,
      layout: $(go.TreeLayout,
        {
          comparer: go.LayoutVertex.standardComparer,

          angle: 90
        }) // have the comparer sort by numbers as well as letters
      // other properties are set by the layout function, defined below
    });

    dia.commandHandler.archetypeGroupData = { key: 'Group', isGroup: true };


    const makePort = function (id: string, spot: go.Spot) {
      return $(go.Shape, 'Circle',
        {
          opacity: .5,
          fill: 'gray', strokeWidth: 0, desiredSize: new go.Size(8, 8),
          portId: id, alignment: spot,
          fromLinkable: true, toLinkable: true
        }
      );
    }

    // define the Node template
    dia.nodeTemplate =
      $(go.Node, 'Spot',
        {
          contextMenu:
            $('ContextMenu',
              $('ContextMenuButton',
                $(go.TextBlock, 'Group'),
                { click: function (e, obj) { e.diagram.commandHandler.groupSelection(); } },
                new go.Binding('visible', '', function (o) {
                  return o.diagram.selection.count > 1;
                }).ofObject())
            )
        },
        $(go.Panel, 'Auto',
          $(go.Shape, 'circle', { stroke: null },
            new go.Binding('fill', 'color')
          ),
          $(go.TextBlock, { margin: 8 },
            new go.Binding('text', 'key'))
        ),
        // Ports
        makePort('t', go.Spot.TopCenter),
        // makePort('l', go.Spot.Left),
        // makePort('r', go.Spot.Right),
        makePort('b', go.Spot.BottomCenter)
      );

    return dia;
  }

  public diagramNodeData: Array<go.ObjectData> = [
    { key: 'ROOT', color: 'lightblue' },
  ];
  public diagramLinkData: Array<go.ObjectData> = [
    // { key: -1, from: 'Alpha', to: 'Beta', fromPort: 'r', toPort: '1' },
  ];
  public diagramDivClassName: string = 'myDiagramDiv';
  public diagramModelData = { prop: 'value' };
  public skipsDiagramUpdate = false;

  // When the diagram model changes, update app data to reflect those changes
  public diagramModelChange = function (changes: go.IncrementalData) {
    // when setting state here, be sure to set skipsDiagramUpdate: true since GoJS already has this update
    // (since this is a GoJS model changed listener event function)
    // this way, we don't log an unneeded transaction in the Diagram's undoManager history
    this.skipsDiagramUpdate = true;

    this.diagramNodeData = DataSyncService.syncNodeData(changes, this.diagramNodeData);
    this.diagramLinkData = DataSyncService.syncLinkData(changes, this.diagramLinkData);
    this.diagramModelData = DataSyncService.syncModelData(changes, this.diagramModelData);
  };

  public initPalette(): go.Palette {
    const $ = go.GraphObject.make;
    const palette = $(go.Palette);

    palette.nodeTemplate =
      $(go.Node, 'Auto',
        // $(go.Shape, {
        //   figure: 'circle', strokeWidth: 3, fill: 'white'
        // }, new go.Binding('figure', 'shape'), new go.Binding('stroke', 'color')),
        // $(go.TextBlock, {
        //   font: 'bold 20px Courier', textAlign: 'center', margin: 10
        // }, new go.Binding('text', 'key')),
        $(go.Panel, "Vertical",
        $(go.Shape, {
          figure: 'circle', strokeWidth: 3, fill: 'white',  alignment: go.Spot.Bottom, stretch: go.GraphObject.Horizontal,
          height: 40, width: 45 , margin: 20
        }, new go.Binding('figure', 'shape'), new go.Binding('stroke', 'color')),
        $(go.TextBlock, {
          font: 'bold 20px Courier', margin: 5
        }, new go.Binding('text', 'key')))
      )

    palette.model = $(go.GraphLinksModel,
      {
        linkKeyProperty: 'key'  // IMPORTANT! must be defined for merges and data sync when using GraphLinksModel
      });

    return palette;
  }
  public paletteNodeData: Array<go.ObjectData> = [
    { key: 'ROOT', color: 'lightblue' },
    { key: 'AND', color: 'red', shape: 'andgate' },
    { key: 'OR', color: 'lightgreen', shape: 'orgate' },
    { key: 'LEAF', color: 'black' }
  ];
  public paletteLinkData: Array<go.ObjectData> = [
    {}
  ];
  public paletteModelData = { prop: 'val' };
  public paletteDivClassName = 'myPaletteDiv';
  public skipsPaletteUpdate = false;
  public paletteModelChange = function (changes: go.IncrementalData) {
    // when setting state here, be sure to set skipsPaletteUpdate: true since GoJS already has this update
    // (since this is a GoJS model changed listener event function)
    // this way, we don't log an unneeded transaction in the Palette's undoManager history
    this.skipsPaletteUpdate = true;

    this.paletteNodeData = DataSyncService.syncNodeData(changes, this.paletteNodeData);
    this.paletteLinkData = DataSyncService.syncLinkData(changes, this.paletteLinkData);
    this.paletteModelData = DataSyncService.syncModelData(changes, this.paletteModelData);
  };

  //added dependecy injection for api service
  constructor(private cdr: ChangeDetectorRef, private apiService: ApiService) { }

  // Overview Component testing
  public oDivClassName = 'myOverviewDiv';
  public initOverview(): go.Overview {
    const $ = go.GraphObject.make;
    const overview = $(go.Overview);
    return overview;
  }
  public observedDiagram = null;

  // currently selected node; for inspector
  public selectedNode: go.Node | null = null;

  public ngAfterViewInit() {

    if (this.observedDiagram) return;
    this.observedDiagram = this.myDiagramComponent.diagram;
    this.cdr.detectChanges(); // IMPORTANT: without this, Angular will throw ExpressionChangedAfterItHasBeenCheckedError (dev mode only)

    const appComp: AppComponent = this;
    // listener for inspector
    this.myDiagramComponent.diagram.addDiagramListener('ChangedSelection', function (e) {
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


  public handleInspectorChange(newNodeData) {
    const key = newNodeData.key;
    // find the entry in nodeDataArray with this key, replace it with newNodeData
    let index = null;
    for (let i = 0; i < this.diagramNodeData.length; i++) {
      const entry = this.diagramNodeData[i];
      if (entry.key && entry.key === key) {
        index = i;
      }
    }

    if (index >= 0) {
      // here, we set skipsDiagramUpdate to false, since GoJS does not yet have this update
      this.skipsDiagramUpdate = false;
      this.diagramNodeData[index] = _.cloneDeep(newNodeData);
    }
  }


}
