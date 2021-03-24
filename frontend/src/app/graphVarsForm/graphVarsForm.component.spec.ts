import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GraphVarsForm } from './graphVarsForm.component';

describe('GraphVarsFormComponent', () => {
  let component: GraphVarsForm;
  let fixture: ComponentFixture<GraphVarsForm>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GraphVarsForm ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GraphVarsForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
