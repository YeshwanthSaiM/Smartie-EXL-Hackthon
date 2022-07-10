import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FrontDisplayComponent } from './front-display.component';

describe('FrontDisplayComponent', () => {
  let component: FrontDisplayComponent;
  let fixture: ComponentFixture<FrontDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FrontDisplayComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FrontDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
