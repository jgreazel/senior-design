import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AdInspectorComponent } from './adInspector.component';

describe('InspectorComponent', () => {
  let component: AdInspectorComponent;
  let fixture: ComponentFixture<AdInspectorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AdInspectorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdInspectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
