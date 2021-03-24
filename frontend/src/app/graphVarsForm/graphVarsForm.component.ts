import { Component, EventEmitter, Inject, Input, Output } from '@angular/core';

@Component({
    selector: 'graph-vars-form',
    templateUrl: './graphVarsForm.component.html',
    styleUrls: ['./graphVarsForm.component.css']
})
export class GraphVarsForm {

    data = {
        acceptableRiskThreshold: 0,
        defenseBudget: 0
    }

    @Input()
    public isDefense: boolean;

    @Output()
    public onFormChange: EventEmitter<any> = new EventEmitter<any>();

    public onCommitForm() {
        this.onFormChange.emit(this.data);
    }

}