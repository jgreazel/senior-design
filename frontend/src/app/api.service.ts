import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import * as go from 'gojs';


// for running fake backend: 
// make sure json server is installed globally with 'npm i -g json-server'
// after navigationg to app folder, start server with 'json-sever --watch db.json'

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
  computeNodeData(nodeData: go.ObjectData): Observable<any> {
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify(nodeData);
    console.log(body)
    return this.http.post(this.baseURL + 'nodeData', body, {'headers':headers})
  }
 
}
