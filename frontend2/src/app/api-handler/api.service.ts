import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import * as go from 'gojs';

@Injectable({ providedIn: 'root' })
export class ApiService {

  attackURL :string = "http://127.0.0.1:8000/api/attack/";
  attackDefenseURL :string = "http://127.0.0.1:8000/api/attack-defense/";
  gameTheoryURL :string = "http://127.0.0.1:8000/api/game-theory/";

  constructor(private http: HttpClient) {
  }

  // example of a get request
  getNodeData(): Observable<Array<go.ObjectData>> {
    console.log('get sample nodes ' + this.attackURL)
    return this.http.get<Array<go.ObjectData>>(this.attackURL)
  }

  /**
   * Post method to back end for analyzing graph data
   * @param selectedEngine 
   * @param acceptableRiskThreshold 
   * @param defenseBudget 
   * @param nodeData 
   * @param edgeData 
   * @returns Analyzed results from the back end
   */
  analyzeData(selectedEngine: string, acceptableRiskThreshold: number, defenseBudget: number, nodeData: go.ObjectData, edgeData: go.ObjectData): Observable<any> {
    const headers = { 'content-type': 'application/json' }
    const body = selectedEngine == 'Attack Tree' ? { 'selectedEngine': selectedEngine, 'acceptableRiskThreshold': acceptableRiskThreshold, 'nodeData': nodeData, 'edgeData': edgeData } :
    { 'selectedEngine': selectedEngine, 'acceptableRiskThreshold': acceptableRiskThreshold, 'defenseBudget': defenseBudget, 'nodeData': nodeData, 'edgeData': edgeData };
    console.log(JSON.stringify(body))
    if(selectedEngine == 'attackTree'){
      return (
        this.http.post(this.attackURL,
          JSON.stringify(body), { 'headers': headers })
      )
      }
      if(selectedEngine == 'attackDefenseTree'){
        return (
          this.http.post(this.attackDefenseURL,
            JSON.stringify(body), { 'headers': headers })
        )
        }
      else{
        return (
          this.http.post(this.gameTheoryURL,
            JSON.stringify(body), { 'headers': headers })
        )
      }
  }
}
