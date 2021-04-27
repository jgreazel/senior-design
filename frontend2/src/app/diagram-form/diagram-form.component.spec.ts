import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DiagramFormComponent } from './diagram-form.component';

describe('DiagramFormComponent', () => {
  let component: DiagramFormComponent;
  let fixture: ComponentFixture<DiagramFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DiagramFormComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DiagramFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
