import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import * as go from 'gojs';


@Injectable({providedIn:'root'})
export class ApiService {
 
  baseURL: string = "http://localhost:3000/";
 
  constructor(private http: HttpClient) {
  }
 
    // example of a get request
//   getPeople(): Observable<Person[]> {
//     console.log('getPeople '+this.baseURL + 'people')
//     return this.http.get<Person[]>(this.baseURL + 'people')
//   }
 
  computeNodeData(nodeData: Array<go.ObjectData>): Observable<any> {
    const headers = { 'content-type': 'application/json'}  
    const body=JSON.stringify(nodeData);
    console.log(body)
    return this.http.post(this.baseURL + 'nodeData', body,{'headers':headers})
  }
 
}
