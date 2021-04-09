import { Component } from '@angular/core';
import * as go from 'gojs';
import { DataSyncService } from 'gojs-angular';


@Component({
  selector: 'atk-def-tree-palette',
  templateUrl: './atk-def-tree-palette.component.html',
  styleUrls: ['./atk-def-tree-palette.component.css']
})
export class AtkDefTreePaletteComponent {

  public initPalette(): go.Palette {
    const $ = go.GraphObject.make;
    const palette = $(go.Palette);

    palette.nodeTemplate =
      $(go.Node, 'Auto',
      { selectionAdorned: false},
        $(go.Panel, "Vertical",
          $(go.Shape, {
            figure: 'circle',
            strokeWidth: 3,
            fill: 'white',
            alignment: go.Spot.Bottom,
            stretch: go.GraphObject.Horizontal,
            height: 40,
            width: 45,
            margin: new go.Margin(70, 25, 10, 25),
          }, new go.Binding('figure', 'shape'),
            new go.Binding('stroke', 'color')),
          $(go.TextBlock, {
            font: 'bold 20px Courier',
            margin: 5
          }, new go.Binding('text', 'key')))
      )

    palette.model = $(go.GraphLinksModel,
      {
        linkKeyProperty: 'key'  // IMPORTANT! must be defined for merges and data sync when using GraphLinksModel
      });
    return palette;
  }

  public atkTreePalette = [
    { key: 'AND', color: 'red', shape: 'andgate' },
    { key: 'OR', color: 'green', shape: 'orgate' },
    { key: 'ROOT_NODE', text: 'Root Node', color: 'purple', shape: 'orgate', impact: 0 },
    { key: 'LEAF', text: 'placeholderText', preDefenseProbability: 0, postDefenseProbability: 0, color: 'blue', shape: 'square', probability: 0, cost: 0 },
    { key: 'SAFE_PATH', text: 'Safe Path', probability: 0, color: 'lightblue', shape: 'square' },
    { key: 'DEFENSE_NODE', text: 'Defense', defenseCost: 0, cost: 0, color: 'yellow', shape: 'circle' }
  ];

  public paletteNodeData: Array<go.ObjectData> = this.atkTreePalette;

  public paletteLinkData: Array<go.ObjectData> = [

  ];

  public paletteModelData = { prop: 'val' };
  public paletteDivClassName = 'paletteDiv';
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
}
