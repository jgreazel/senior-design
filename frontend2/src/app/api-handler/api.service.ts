import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import * as go from 'gojs';

@Injectable({ providedIn: 'root' })
export class ApiService {

  baseURL: string = "http://127.0.0.1:8000/api/hello-view/";

  constructor(private http: HttpClient) {
  }

  // example of a get request
  getNodeData(): Observable<Array<go.ObjectData>> {
    console.log('get sample nodes ' + this.baseURL)
    return this.http.get<Array<go.ObjectData>>(this.baseURL)
  }

  // example of a post request
  analyzeData(selectedEngine: string, acceptableRiskThreshold: number, defenseBudget: number, nodeData: go.ObjectData, edgeData: go.ObjectData): Observable<any> {
    const headers = { 'content-type': 'application/json' }
    const body = selectedEngine == 'Attack Tree' ? { 'selectedEngine': selectedEngine, 'acceptableRiskThreshold': acceptableRiskThreshold, 'nodeData': nodeData, 'edgeData': edgeData } :
    { 'selectedEngine': selectedEngine, 'acceptableRiskThreshold': acceptableRiskThreshold, 'defenseBudget': defenseBudget, 'nodeData': nodeData, 'edgeData': edgeData };
    console.log(JSON.stringify(body))
    return (
      this.http.post(this.baseURL,
        JSON.stringify(body), { 'headers': headers })
    )
  }
}
