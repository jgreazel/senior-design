import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import * as go from 'gojs';

/**
 * For running fake backed:
 * make sure json server is installed globally with 'npm i -g json-server'
 * after navigating to app folder, start server with 'json-server --watch db.json
 */

@Injectable({providedIn:'root'})
export class ApiService {
 
  baseURL: string = "http://localhost:3000/";
 
  constructor(private http: HttpClient) {
  }
 
  // example of a get request
  getNodeData(): Observable<Array<go.ObjectData>> {
    console.log('get sample nodes '+ this.baseURL + 'nodeData')
    return this.http.get<Array<go.ObjectData>>(this.baseURL + 'nodeData')
  }
 
  // example of a post request
  analyzeData(nodeData: go.ObjectData, edgeData: go.ObjectData): Observable<any> {
    const headers = { 'content-type': 'application/json'}  
    const body = {'nodeData': nodeData, 'edgeData': edgeData};
    console.log(JSON.stringify(body))
    return (
      this.http.post(this.baseURL + 'nodeData', 
      JSON.stringify(body), {'headers': headers})
    )
  }
}
