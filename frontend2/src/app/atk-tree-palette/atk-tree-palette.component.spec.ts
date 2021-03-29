import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AtkTreePaletteComponent } from './atk-tree-palette.component';

describe('AtkTreePaletteComponent', () => {
  let component: AtkTreePaletteComponent;
  let fixture: ComponentFixture<AtkTreePaletteComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AtkTreePaletteComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AtkTreePaletteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
