import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GameTheoryFormComponent } from './game-theory-form.component';

describe('GameTheoryFormComponent', () => {
  let component: GameTheoryFormComponent;
  let fixture: ComponentFixture<GameTheoryFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GameTheoryFormComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GameTheoryFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
