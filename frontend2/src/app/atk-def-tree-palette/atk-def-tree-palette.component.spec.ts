import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AtkDefTreePaletteComponent } from './atk-def-tree-palette.component';

describe('AtkDefTreePaletteComponent', () => {
  let component: AtkDefTreePaletteComponent;
  let fixture: ComponentFixture<AtkDefTreePaletteComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AtkDefTreePaletteComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AtkDefTreePaletteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
