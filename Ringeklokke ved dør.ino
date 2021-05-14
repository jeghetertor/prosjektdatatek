#include <CircusESP32Lib.h>

// CoT variabler
char ssid[] = "Trappegata 8";         //char ssid[] = "Tor sin iPhone";
char password[] = "Vidgar&Torunn";    //char password[] = "fch29tbpfjf6";

char token[] = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0OTk0In0.U2OYCiZTQR1tyb9o-E-mssfC1Xtu0wuTXUwgSpmsri0";
char server[] = "www.circusofthings.com";
char order_key_LED[] = "3900";
char resultat_key[] = "21861";
char send_key[] = "14157";
char innstilling_key[] = "27790"; 
char svar_ringing_key[] = "412";
CircusESP32Lib circusESP32(server, ssid, password);

// Variabler for ringeklokkelogikk
int ringe_mode = 0;
int ringe_svar = 0;
int tellevar_old = 0;
bool slipp_inn = false;

// Variabler for 7-segment
bool bPress = false;
bool buttonPin_2_state = false;
bool buttonPin_2_state_old = false;
int buttonPushCounter = 0;
int buttonState = 0;
int lastButtonState = 0;
     
// Variabler for inn-/utganger
const int a = 12; // segment  "a" lyser
const int b = 14; // segment  "b" lyser
const int c = 27; // segment  "c" lyser
const int d = 26; // segment  "d" lyser
const int e = 25; // segment  "e" lyser
const int f = 5; // segment  "f" lyser
const int g = 18; // segment  "g" lyser

const int red_light = 4;
const int yellow_light = 16;
const int green_light = 17;

const int buttonPin = 2;
const int buttonPin_2 = 19;

void setup() {
 pinMode(a,OUTPUT); // A
 pinMode(b,OUTPUT); // B
 pinMode(c,OUTPUT); // C
 pinMode(d,OUTPUT); // D
 pinMode(e,OUTPUT); // E
 pinMode(f,OUTPUT); // F
 pinMode(g,OUTPUT); // G

 pinMode(red_light,OUTPUT);
 pinMode(yellow_light,OUTPUT);
 pinMode(green_light,OUTPUT);
   
 pinMode(buttonPin,INPUT_PULLUP);
 pinMode(buttonPin_2, INPUT);
 Serial.begin(115200);
 circusESP32.begin();
 Serial.println("CoT - ESP32");
 displayDigit(buttonPushCounter);
 }

void loop() {
  if(ringe_mode == 0){  //Her velger du hvilken beboer som skal ringes og gir ringesingnal
    lys_av();
    int tellevar = Counter();
    buttonPin_2_state = digitalRead(buttonPin_2);
    if(tellevar_old != tellevar){
      circusESP32.write(innstilling_key, tellevar,token);
      tellevar_old = tellevar;
    }
    if(buttonPin_2_state != buttonPin_2_state_old){
      if(buttonPin_2){
        buttonPin_2_state_old = buttonPin_2_state;
        ringe_mode = 1;
      }
      buttonPin_2_state_old = buttonPin_2_state;
    }
  }
  else if(ringe_mode == 1){  //Her sendes ringesignalet og mottar svar 
    circusESP32.write(send_key, buttonPin_2_state,token);
    ringe_svar = circusESP32.read(svar_ringing_key, token);
    switch(ringe_svar){
      case 0:
        digitalWrite(yellow_light, HIGH);
        break;
      case 1: //Slipp inn
        digitalWrite(yellow_light, LOW);
        digitalWrite(green_light, HIGH);
        slipp_inn = true;
        ringe_mode = 2;
        break;
      case 2: //Ikke slipp inn
        digitalWrite(yellow_light, LOW);
        digitalWrite(red_light, HIGH);
        slipp_inn = false;
        ringe_mode = 2;
        break;
    default:
    break;
    }
  }
  else if(ringe_mode == 2){  // Her aktiveres svaret på ringingen og resetter.
    if(slipp_inn){
        // HER KAN DET SETTES INN FUNKSJON FOR ÅPNING AV LÅSESYLINDER --------
        delay(1000);
        buttonPin_2_state_old = 0;
        ringe_mode = 0;
        circusESP32.write(send_key, 0,token);
      }
      else{
        delay(1000);
        buttonPin_2_state_old = 0;
        ringe_mode = 0;
        circusESP32.write(send_key, 0,token);
      }
  }
}

void lys_av(){ // Skrur av LED lys
  digitalWrite(green_light, LOW);
  digitalWrite(yellow_light, LOW);
  digitalWrite(red_light, LOW);
}

 void displayDigit(int digit){ // Her sendes tall til 7-segment displayet
   //tilstand for segment a
   if(digit != 1 && digit !=4)
   digitalWrite(a,LOW);
   
   //tilstand for segment b
   if(digit != 5  && digit != 6)
   digitalWrite(b,LOW);
   
   //ctilstand for segment c
   if(digit != 2)
   digitalWrite(c,LOW);
   
   //tilstand for segment d
   if(digit != 1 && digit !=4 && digit != 7)
   digitalWrite(d,LOW);
   
   //tilstand for segment e
   if(digit ==2 || digit ==6 || digit ==8 || digit == 0)
   digitalWrite(e,LOW);
   
   //tilstand for segment f
   if(digit !=1 && digit !=2 && digit !=3 && digit !=7)
   digitalWrite(f,LOW);
   
   //tilstand for segment g
   if(digit !=0 && digit !=1 && digit!=7)
   digitalWrite(g,LOW);
 }

 int Counter() { // Her telles det oppover til 6 med knapp
   buttonState=digitalRead(buttonPin);
   if(buttonState!=lastButtonState) //sammenlikne buttonState med den tidligere tilstanden
   {
     //if the state has changed,increment the counter
     if(buttonState==LOW) //hvis tilstanden er endret, øker telleren
     {
       //hvis tilstanden er HIGH har knappen gått fra OFF til ON, ellers gikk den fra OFF til ON
       bPress=true;
       buttonPushCounter++;
       if(buttonPushCounter>4) buttonPushCounter=1;
     }
     delay(500); //delay for å unngå at den "hopper"
   }
   //lagre nåværende tilstand som siste tilstand for riktig tid gjennom loopen
   lastButtonState=buttonState;
   
   if(bPress){
     turnoff();
     displayDigit(buttonPushCounter);
   }
   return buttonPushCounter;
   
 }
 
 void turnoff() {  // Nullstiller 7-segment displayet
   digitalWrite(a,HIGH);
   digitalWrite(b,HIGH);
   digitalWrite(c,HIGH);
   digitalWrite(d,HIGH);
   digitalWrite(e,HIGH);
   digitalWrite(f,HIGH);
   digitalWrite(g,HIGH);
 }
