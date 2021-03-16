import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AdTreePalette } from './adTreePalette.component';

describe('AdTreePalette', () => {
  let component: AdTreePalette;
  let fixture: ComponentFixture<AdTreePalette>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AdTreePalette ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdTreePalette);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
