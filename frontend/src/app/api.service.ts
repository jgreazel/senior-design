import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import * as go from 'gojs';

/**
 * For running fake backed:
 * make sure json server is installed globally with 'npm i -g json-server'
 * after navigating to app folder, start server with 'json-server --watch db.json
 */

@Injectable({ providedIn: 'root' })
export class ApiService {

  // baseURL: string = "http://127.0.0.1:8000/api/hello-view/";//"http://localhost:3000/";
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

  // example of a post request
  analyzeData(selectedEngine: string, acceptableRiskThreshold: number, defenseBudget: number, nodeData: go.ObjectData, edgeData: go.ObjectData): Observable<any> {
    console.log(selectedEngine)
    const headers = { 'content-type': 'application/json' }
    const body = selectedEngine == 'Attack Tree' ? { 'selectedEngine': selectedEngine, 'acceptableRiskThreshold': acceptableRiskThreshold, 'nodeData': nodeData, 'edgeData': edgeData } :
    { 'selectedEngine': selectedEngine, 'acceptableRiskThreshold': acceptableRiskThreshold, 'defenseBudget': defenseBudget, 'nodeData': nodeData, 'edgeData': edgeData };
    console.log(JSON.stringify(body))
    if(selectedEngine == 'Attack Tree'){
      return (
        this.http.post(this.attackURL,
          JSON.stringify(body), { 'headers': headers })
      )
      }
      if(selectedEngine == 'Attack-Defense Tree'){
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
