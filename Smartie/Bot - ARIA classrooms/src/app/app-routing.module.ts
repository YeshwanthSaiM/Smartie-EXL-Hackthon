import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { VtComponent } from './components/vt/vt.component';
import { HomeComponent } from './home/home.component';
const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'vt', component: VtComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
