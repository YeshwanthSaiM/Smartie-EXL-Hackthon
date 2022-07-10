import { Component, OnInit } from '@angular/core';


@Component({
  selector: 'app-vt',
  templateUrl: './vt.component.html',
  styleUrls: ['./vt.component.css']
})
export class VtComponent implements OnInit {

  constructor() { }
  name = "classrooms"
  url = "";





  // :: create a Lex audio client
  // lexAudioClient = new LexAudioClient(this.client)
  // End of lex runtime

  public loadjs(url: string) {
    const body = <HTMLDivElement>document.body;
    const script = document.createElement('script');
    script.innerHTML = '';
    script.src = url;
    script.async = true;
    script.defer = true;
    body.appendChild(script)
  }
  ngOnInit(): void {
    this.loadjs("../../../assets/classrooms/index.js");



    // Here we make the chatbot
    /**
     * functionality:
     * on init: chatbot gets live
     * background init message based on the landing 360 image
     * based on instruction => navigate to next image
     * once next 360 image is loaded, explanation for that image
     */

    /**
     * Try with : lex-audio-client
     */

  }


}
