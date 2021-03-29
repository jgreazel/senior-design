import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AtkDefTreeFormComponent } from './atk-def-tree-form.component';

describe('AtkDefTreeFormComponent', () => {
  let component: AtkDefTreeFormComponent;
  let fixture: ComponentFixture<AtkDefTreeFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AtkDefTreeFormComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AtkDefTreeFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
