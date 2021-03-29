import { ViewChild } from '@angular/core';
import { Component } from '@angular/core';
import * as go from 'gojs';
import { DataSyncService, DiagramComponent } from 'gojs-angular';

@Component({
  selector: 'diagram-canvas',
  templateUrl: './diagram-canvas.component.html',
  styleUrls: ['./diagram-canvas.component.css']
})
export class DiagramCanvasComponent {

  @ViewChild('diagramDiv', { static: true }) public myDiagramComponent: DiagramComponent;

  public initDiagram(){

    //create custom shape for and-gate
    go.Shape.defineFigureGenerator("AndGate", function (shape, w, h) {
      var geo = new go.Geometry();
      var cpOffset = (4 * ((Math.sqrt(2) - 1) / 3)) * .5;
      var fig = new go.PathFigure(0, 0, true);
      geo.add(fig);
      h = 2 * h;
      w = 1.5 * w;
      // The gate body
      fig.add(new go.PathSegment(go.PathSegment.Line, .5 * w, 0));
      fig.add(new go.PathSegment(go.PathSegment.Bezier, w, .5 * h, (.5 + cpOffset) * w, 0,
        w, (.5 - cpOffset) * h));
      fig.add(new go.PathSegment(go.PathSegment.Bezier, .5 * w, h, w, (.5 + cpOffset) * h,
        (.5 + cpOffset) * w, h));
      fig.add(new go.PathSegment(go.PathSegment.Line, 0, h).close());

      geo.rotate(270, w / 3, h / 2)
      geo.offset(0, -h / 6)
      geo.spot1 = go.Spot.TopLeft;
      geo.spot2 = go.Spot.BottomRight;
      return geo;
    })

    //create custom shape for or-gate
    go.Shape.defineFigureGenerator("OrGate", function (shape, w, h) {
      var geo = new go.Geometry();
      var radius = .5;
      var cpOffset = (4 * ((Math.sqrt(2) - 1) / 3)) * radius;
      var centerx = 0;
      var centery = .5;
      var fig = new go.PathFigure(0, 0, true);
      geo.add(fig);
      h = 2 * h;
      w = 1.5 * w;

      fig.add(new go.PathSegment(go.PathSegment.Bezier, w, .5 * h, (centerx + cpOffset + cpOffset) * w, (centery - radius) * h,
        .8 * w, (centery - cpOffset) * h));
      fig.add(new go.PathSegment(go.PathSegment.Bezier, 0, h, .8 * w, (centery + cpOffset) * h,
        (centerx + cpOffset + cpOffset) * w, (centery + radius) * h));
      fig.add(new go.PathSegment(go.PathSegment.Bezier, 0, 0, .25 * w, .75 * h, .25 * w, .25 * h).close());
      geo.rotate(270, w / 3, h / 2)
      geo.offset(0, -h / 6)
      geo.spot1 = new go.Spot(.2, .25);
      geo.spot2 = new go.Spot(.75, .75);
      return geo;
    });

    const $ = go.GraphObject.make;
    const dia = $(go.Diagram, {
      'undoManager.isEnabled': true,
      initialAutoScale: go.Diagram.UniformToFill,
      model: $(go.GraphLinksModel,
        {
          linkToPortIdProperty: 'toPort',
          linkFromPortIdProperty: 'fromPort',
          linkKeyProperty: 'key' // IMPORTANT! must be defined for merges and data sync when using GraphLinksModel
        }
      ),
      layout: $(go.TreeLayout, { isInitial: true, isOngoing: false }),
      "InitialLayoutCompleted": function (e) {
        // if not all Nodes have real locations, force a layout to happen
        if (!e.diagram.nodes.all(function (n) { return n.location.isReal(); })) {
          e.diagram.layoutDiagram(true);
        }
      }
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
      $(go.Node, 'Auto',
        {
          selectionAdorned: true,
        },
        $(go.TextBlock, {
          font: '15px Courier'
        }, new go.Binding('text').makeTwoWay()),
        $(go.Panel, "Vertical",
          $(go.Shape, {
            figure: 'circle',
            strokeWidth: 3,
            fill: 'white',
            alignment: go.Spot.Bottom,
            stretch: go.GraphObject.Horizontal,
            height: 40,
            width: 45,
            margin: 20
          }, new go.Binding('figure', 'shape'),
            new go.Binding('stroke', 'color'))),
        makePort('t', go.Spot.TopCenter),
        makePort('b', go.Spot.BottomCenter)
      )
    return dia;
  }

  // Nodes in the graph
  public diagramNodeData: Array<go.ObjectData> = [

  ];
  // Links in the graph
  public diagramLinkData: Array<go.ObjectData> = [

  ];

  public diagramDivClassName: string = 'diagramDiv';
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
}
