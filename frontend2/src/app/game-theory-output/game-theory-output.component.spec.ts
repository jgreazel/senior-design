import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GameTheoryOutputComponent } from './game-theory-output.component';

describe('GameTheoryOutputComponent', () => {
  let component: GameTheoryOutputComponent;
  let fixture: ComponentFixture<GameTheoryOutputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GameTheoryOutputComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GameTheoryOutputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
