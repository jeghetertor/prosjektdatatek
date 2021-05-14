#include <ESP32Servo.h>
#include <ESP32Tone.h>
#include <ESP32PWM.h>
#include <CircusESP32Lib.h> // Biblioteket til Circus of Things.
#include <analogWrite.h>
#include <pitches.h>

char ssid[] = ""; // Skriv inn navnet til ruteren din her.
char password[] = ""; // Skriv inn passordet til ruteren din her.
char server[] = "www.circusofthings.com"; // Her ligger serveren.
CircusESP32Lib circusESP32(server,ssid,password);

char key_fan[] = "29211";//Vifte key 
char key_window[] = "28932";//Vindu key
char key_LightSwitchKitchen[] = "233"; //Lysbryter key kjøkken
char key_LightSwitchLiving[] = "11379"; //Lysbryter key stue
char token[] = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0OTk0In0.U2OYCiZTQR1tyb9o-E-mssfC1Xtu0wuTXUwgSpmsri0";

const int tempPin = 34;//temperatur sensor
const int buzzer = 32;//buzzer som lager lyd når det er brann eller ringeklokka går
const int roofKitchenLed = 26;//taklys på kjøkken
const int roofLivingroomLed = 14;//taklys på stue
const int8_t EN1 = 27;//dc-motor styring
const int8_t IN1 = 12;//dc-motor styring
const int8_t IN2 = 13;//dc-motor styring

int freq = 4000;
int channel = 0;
int resolution = 8;

int buzzer_bell = 26;
int tempo = 120; //melodiens tempo i bpm

#define T_C 262
#define T_D 294
#define T_E 330
#define T_F 349
#define T_G 392
#define T_A 440
#define T_Ab 466
#define T_B 493
#define T_C2 523
#define T_D2 587

//arrays med notene til sangene
int AlleFugler_melody[] = {T_C, T_E, T_G, T_C2, T_A, T_C2, T_A, T_G, T_F, T_G, T_E, T_C, T_D, T_C};
int MikkelRev_melody[] = {T_E, T_G, T_C, T_E, T_G, T_C, T_F, T_A, T_C2, T_A, T_A, T_G};
int LisaGikkTilSkolen_melody[] = {T_C, T_D, T_E, T_F, T_G, T_G, T_A, T_A, T_A, T_A, T_G, T_F, T_F, T_F, T_F, T_E, T_E, T_D, T_D, T_D, T_D, T_C};
int LilleMaltrost_melody[] = {T_E, T_F, T_G, T_G, T_E, T_F, T_G, T_G, T_A, T_G, T_F, T_F, T_E, T_D};
int BjornenSover_melody[] = {T_C, T_C, T_C, T_E, T_D, T_D, T_D, T_F, T_E, T_E, T_D, T_D, T_C};
int BamsesFodselsdag_melody[] = {T_C2, T_D2, T_C2, T_D2, T_C2, T_D2, T_C2, T_D2, T_C2, T_Ab, T_G, T_E, T_F};

//notenes varighet i sangene
//tre fjerdedelsnote har varighet 6, en kvartnote har varighet 4 og halvnote har varighet 2
int AlleFugler_durations[] = {2, 4, 4, 4, 4, 6, 6, 2, 4, 6, 4, 4, 2, 2};
int MikkelRev_durations[] = {4, 4, 2, 4, 4, 2, 4, 4, 4, 4, 2, 2};
int LisaGikkTilSkolen_durations[] = {4, 4, 4, 4, 2, 2, 4, 4, 4, 4, 2, 4, 4, 4, 4, 2, 2, 4, 4, 4, 4, 2};
int LilleMaltrost_durations[] = {6, 6, 4, 4, 6, 6, 4, 4, 6, 6, 4, 4, 4, 4, 2};
int BjornenSover_durations[] = {4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2};
int BamsesFodselsdag_durations[] = {4, 4, 4, 4, 4, 4, 4, 6, 4, 4, 4, 4, 2};

Servo myservo;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid,password);
  circusESP32.begin();
  myservo.attach(25);

  pinMode(EN1, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(roofKitchenLed,OUTPUT);
  digitalWrite(roofKitchenLed, LOW);
  pinMode(roofLivingroomLed,OUTPUT);
  digitalWrite(roofLivingroomLed, LOW);
  
  ledcSetup(3,8000,12);// Setter PWM funksjoner
  ledcAttachPin(buzzer,3); 

  ledcSetup(channel, freq, resolution);
  ledcAttachPin(buzzer_bell, channel);

  Serial.println();
  Serial.print("Connecting");
  while( WiFi.status() != WL_CONNECTED ){
      delay(500);
      Serial.print(".");        
  }
}

void loop() {
  light(roofKitchenLed, key_LightSwitchKitchen);//lysbryter kjøkken
  light(roofLivingroomLed, key_LightSwitchLiving);//lysbryter stue
  firealarm(50);//brann ve 50 grader celsius
  setFan();//kjøkkenvifte
  setWindow();//vindu i stua
}

//temperaturmåling
int getTemp(int tempPin){//returnerer temperatur
  int reading = analogRead(tempPin);//leser verdi fra temp sensor
  float voltage = reading/1025.0;// konverterer reading til spenning for 3.3v
  float temperature = (voltage - 0.5) * 100 ;  //konverterer til grader((spenning - 500mV)* 100)
  Serial.print(temperature); Serial.println(" degrees C");
  return temperature;
}

//lysbryter stue og kjøkken
void light(int roofLed, char key[]) {// Her styres taklys gjennom CoT
  int light_value = circusESP32.read(key,token);
  if (light_value == 1){
    digitalWrite(roofLed, HIGH); // Skru led på dersom knappen trykkes ON
  } 
  else{
    digitalWrite(roofLed, LOW);// Skru led av dersom knappen trykkes OFF
  }
}

//brannalarm
void firealarm(int fireTemp){//lager lyd om temperatur fra funksjon getTemp er større enn en valgt parameter verdi fireTemp
  if(getTemp(tempPin) >= fireTemp){
    for(int i = 1000; i<=3000; i+=500){//lager melodi ved brann
      ledcWriteTone(3, i);
      delay(300);
    }
    ledcWriteTone(3, 0);
    delay(50);
  }
}

//vindu
void setWindow(){
  //JUSTERE VINDU VINKEL
  int vindu_value = circusESP32.read(key_window,token);//Henter verdi fra signal vindu i circus
  myservo.write(vindu_value);//servo roterer mellom 0-50 grader, avhengig av circus
}

//vifte
void setFan(){
  //JUSTERE VIFTE FREKVENS
  int vifte_value = circusESP32.read(key_fan,token);//leser verdi fra Circus
  //får inn verdi mellom 0-100 fra vifte_value
  vifte_value = map(vifte_value, 0,100 , 0, 510); //og gir ut tilsvarende verdi på intervallet 0-510
  digitalWrite(IN1, LOW);//IN1 og IN2 bestemmer retningen
  digitalWrite(IN2, HIGH);
  analogWrite(EN1,vifte_value);//får dc-motor til å snurre rundt
}

//ringeklokke
void PlaySong(int notes[], int durations[], int BPM, int arrSize){ 
  for (int thisNote = 0; thisNote < arrSize; thisNote++) 
  {
    int noteDuration = (int)((750 * (60 * 2 / BPM)) / durations[thisNote] + 0.); //definerer lengden på en tone
    ledcWriteTone(channel, notes[thisNote]);
    ledcWrite(channel, 200);
    delay(noteDuration);

    ledcWrite(channel, 0);
    int pauseBetweenNotes = noteDuration * 1.20; //definerer pause mellom notene som lengden på tonen * 1,2
    delay(pauseBetweenNotes); //lengden på tonen ved definisjonen
  }
  delay(1000); //et sekund pause før neste sang
}
void songnumber(){
  int sangnummer = circusESP32.read("27790", token);
  switch(sangnummer){
    case 0:
      PlaySong(LisaGikkTilSkolen_melody, LisaGikkTilSkolen_durations, tempo,int (sizeof(LisaGikkTilSkolen_melody)/sizeof(int)));
      break;
    case 1:
      PlaySong(MikkelRev_melody, MikkelRev_durations, tempo,int (sizeof(MikkelRev_melody)/sizeof(int)));
      break;
    case 2:
      PlaySong(AlleFugler_melody, AlleFugler_durations, tempo,int (sizeof(AlleFugler_melody)/sizeof(int)));
      break;
    case 3:
      PlaySong(LilleMaltrost_melody, LilleMaltrost_durations, tempo,int (sizeof(LilleMaltrost_melody)/sizeof(int)));
      break;
    case 4:
      PlaySong(BjornenSover_melody, BjornenSover_durations, tempo,int (sizeof(BjornenSover_melody)/sizeof(int)));
      break;
    case 5:
      PlaySong(BamsesFodselsdag_melody, BamsesFodselsdag_durations, tempo,int (sizeof(BamsesFodselsdag_melody)/sizeof(int)));
      break;
  default:
    break;
    }
}
void bell(){
  int ringesignal =  circusESP32.read("28932", token);
    if(ringesignal == 1){
      songnumber();
    }
  
  }

}
