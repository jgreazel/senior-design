import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AttackTreeOutputComponent } from './attack-tree-output.component';

describe('AttackTreeOutputComponent', () => {
  let component: AttackTreeOutputComponent;
  let fixture: ComponentFixture<AttackTreeOutputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AttackTreeOutputComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AttackTreeOutputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
