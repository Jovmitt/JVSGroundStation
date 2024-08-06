
int X_Axis = 1500; //0.0
int Y_Axis = 1500; //0.0
int Slider_Axis = 1000; //0.0
int Z_Axis = 1500; //1.0
int Cam_X = 1500; //0
int Cam_Y = 1500; //0
int AUX = 1500; //0
int MODE = 1000; //0
int Arduino_LED = 0; //0

int LED = 13;
int warningLED = 12;



//////////////////////CONFIGURATION///////////////////////////////
#define CHANNEL_NUMBER 8  //set the number of chanels
#define CHANNEL_DEFAULT_VALUE 1500  //set the default servo value
#define FRAME_LENGTH 22500  //set the PPM frame length in microseconds (1ms = 1000µs)
#define PULSE_LENGTH 300  //set the pulse length
#define onState 1  //set polarity of the pulses: 1 is positive, 0 is negative
#define sigPin 10 //set PPM signal output pin on the arduino
//////////////////////////////////////////////////////////////////

#define SWITCH_PIN 16
#define CHANNEL_TO_MODIFY 7
#define SWITCH_STEP 100

byte previousSwitchValue;

/*this array holds the servo values for the ppm signal
 change theese values in your code (usually servo values move between 1000 and 2000)*/
int ppm[CHANNEL_NUMBER];

int currentChannelStep;



void setup()
{

  Serial.begin(115200);
  Serial.println();
  pinMode(LED, OUTPUT);
  //pinmode(warningLED, OUTPUT);



  previousSwitchValue = HIGH;
  
  //initiallize default ppm values
  for(int i=0; i<CHANNEL_NUMBER; i++){
    if (i == 2 || i == CHANNEL_TO_MODIFY) {
      ppm[i] = 1000;
    } 
    else {
      ppm[i]= CHANNEL_DEFAULT_VALUE;
    }
  }

  pinMode(sigPin, OUTPUT);
  pinMode(SWITCH_PIN, INPUT_PULLUP);
  digitalWrite(sigPin, !onState);  //set the PPM signal pin to the default state (off)
  
  cli();
  TCCR1A = 0; // set entire TCCR1 register to 0
  TCCR1B = 0;
  
  OCR1A = 100;  // compare match register, change this
  TCCR1B |= (1 << WGM12);  // turn on CTC mode
  TCCR1B |= (1 << CS11);  // 8 prescaler: 0,5 microseconds at 16mhz
  TIMSK1 |= (1 << OCIE1A); // enable timer compare interrupt
  sei();

  currentChannelStep = SWITCH_STEP;

}

void SerialEvent()
{
  char characterBuf[46];  //stores incoming
  int incomingLength = 0; //stores incoming length
  char *token;            //token for converting byte array to string array
  int counterNum = 1;


  if (Serial.available()) {
    incomingLength = Serial.readBytesUntil('\n', characterBuf, 50);    //calculate length of byte array
    token = strtok(characterBuf, ",");  //convert to string
    X_Axis = atoi(token);
    while (token != NULL) {   //if token doesnt find another comma it goes back to begginning

      token = strtok(NULL, ",");  //changes token to a string def of NULL
      //      Serial.println(token);

      switch (counterNum) {
        case 1:
          Y_Axis = atoi(token);
          break;

        case 2:
          Slider_Axis = atoi(token);
          break;

        case 3:
          Z_Axis = atoi(token);
          break;

        case 4:
          Cam_X = atoi(token);
          break;

        case 5:
          Cam_Y = atoi(token);
          break;

        case 6:
          AUX = atoi(token);
          break;

        case 7:
          MODE = atoi(token);
          break;

        case 8:
          Arduino_LED = atoi(token);
          break;

      }
      counterNum++;
    }
  }
}

void loop()
{ 

  int switchState;

  switchState = digitalRead(SWITCH_PIN);

  if (switchState == LOW && previousSwitchValue == HIGH) {

    static int val = SWITCH_STEP;

    ppm[CHANNEL_TO_MODIFY] = ppm[CHANNEL_TO_MODIFY] + currentChannelStep;
    
    if (ppm[CHANNEL_TO_MODIFY] > 2000 || ppm[CHANNEL_TO_MODIFY] < 1000) {
      currentChannelStep = currentChannelStep * -1; 
      ppm[CHANNEL_TO_MODIFY] = ppm[CHANNEL_TO_MODIFY] + currentChannelStep;
    }
    
  }

  previousSwitchValue = switchState;
  

  if (Serial.available()) {

    SerialEvent();

    if (Arduino_LED == 1) {
      digitalWrite(LED, HIGH);
    }
    else {
      digitalWrite(LED, LOW);
    }

    int turning_Val = map(X_Axis, 1000, 2000, 0, 300);

    Serial.print(X_Axis);
    Serial.print("  ");
    Serial.print(Y_Axis);
    Serial.print("  ");
    Serial.print(Slider_Axis);
    Serial.print("  ");
    Serial.print(Z_Axis);
    Serial.print("  ");
    Serial.print(Cam_X);
    Serial.print("  ");
    Serial.print(Cam_Y);
    Serial.print("  ");
    Serial.print(AUX);
    Serial.print("  ");
    Serial.print(MODE);
    Serial.print("  ");
    Serial.print(Arduino_LED);
    Serial.print("  ");
    Serial.println(turning_Val);

  } 
  /* else {
    digitalWrite(warningLED, LOW);
    delay(500);
    digitalWrite(warningLED, HIGH);
    MODE = failsafe;
  } */

  ppm[0] = X_Axis;
  ppm[1] = Y_Axis;
  ppm[2] = Slider_Axis;
  ppm[3] = Z_Axis;
  ppm[4] = Cam_X;
  ppm[5] = Cam_Y;
  ppm[6] = AUX;
  ppm[7] = MODE;
  
}

ISR(TIMER1_COMPA_vect){  //leave this alone
  static boolean state = true;
  
  TCNT1 = 0;
  
  if (state) {  //start pulse
    digitalWrite(sigPin, onState);
    OCR1A = PULSE_LENGTH * 2;
    state = false;
  } else{  //end pulse and calculate when to start the next pulse
    static byte cur_chan_numb;
    static unsigned int calc_rest;
  
    digitalWrite(sigPin, !onState);
    state = true;

    if(cur_chan_numb >= CHANNEL_NUMBER){
      cur_chan_numb = 0;
      calc_rest = calc_rest + PULSE_LENGTH;// 
      OCR1A = (FRAME_LENGTH - calc_rest) * 2;
      calc_rest = 0;
    }
    else{
      OCR1A = (ppm[cur_chan_numb] - PULSE_LENGTH) * 2;
      calc_rest = calc_rest + ppm[cur_chan_numb];
      cur_chan_numb++;
    }     
  }
}
