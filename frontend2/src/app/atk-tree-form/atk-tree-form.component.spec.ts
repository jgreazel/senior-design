import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AtkTreeFormComponent } from './atk-tree-form.component';

describe('AtkTreeFormComponent', () => {
  let component: AtkTreeFormComponent;
  let fixture: ComponentFixture<AtkTreeFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AtkTreeFormComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AtkTreeFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
