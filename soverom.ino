#include "time.h"
#include <ESP32Servo.h>
#include <ESP32Tone.h>
#include <ESP32PWM.h>
#include <CircusESP32Lib.h> // Biblioteket til Circus of Things.
#include <analogWrite.h>

char ssid[] = ""; // Skriv inn navnet til ruteren din her.
char password[] = ""; // Skriv inn passordet til ruteren din her.
char server[] = "www.circusofthings.com"; // Her ligger serveren.
CircusESP32Lib circusESP32(server,ssid,password);


char key_fan[] = "7589";//Vifte key 
char key_window[] = "11479";//Vindu key
char key_heater[] = "7025";//Varmeovn key
char key_min_on[] = "926";//Lys minutt key
char key_hour_on[] = "21996";//lys time key
char key_min_off[] = "29488";//Lys minutt key
char key_hour_off[] = "28053";//lys time key
char key_wake_up[] = "28270";//automatiske lys key
char key_LightSwitch[] = "14800"; //Lysbryter key
char token[] = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0OTk0In0.U2OYCiZTQR1tyb9o-E-mssfC1Xtu0wuTXUwgSpmsri0";

const int tempPin = 34;//temperatur sensor
const int heaterLed = 26;//led som lyser rødt når ovnen er på
const int buzzer = 32;//buzzer som lager lyd når det er brann eller ringeklokka går
const int roofLightLed = 14;//taklys på soverom, som vises på eller av med led
const int8_t EN1 = 27;//dc-motor styring
const int8_t IN1 = 12;//dc-motor styring
const int8_t IN2 = 13;//dc-motor styring

const char* ntpServer = "pool.ntp.org";//server som gjør det mulig å synkronisere klokken fra datamaskinen sammen med ESP-en
const long  gmtOffset_sec = 3600;
const int   daylightOffset_sec = 3600;

Servo myservo;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid,password);
  circusESP32.begin();
  myservo.attach(25);
  
  pinMode(heaterLed, OUTPUT);
  pinMode(EN1, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(roofLightLed,OUTPUT);
  digitalWrite(roofLightLed, LOW);
  
  ledcSetup(3,8000,12);// Setter PWM funksjoner
  ledcAttachPin(buzzer,3); 

  Serial.println();
  Serial.print("Connecting");

  while( WiFi.status() != WL_CONNECTED ){
      delay(500);
      Serial.print(".");        
  }
  Serial.println();
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);//
  Serial.println("\nWaiting for Internet time");
  printLocalTime();//printer klokke tiden nå

  while(!time(nullptr)){
     Serial.print("*");
     delay(1000);
  }
  Serial.println("\nTime response....OK");  
}

void loop() {
  
  setFan();//setter vifte hastiget(dc-motor)
  setWindow();//setter vidu vinkel(servo)
  setHeater();//setter led lys av eller på, avhengig av ovn verdi hentet fra CoT
  
  int wake_up_value = circusESP32.read(key_wake_up,token);//henter verdi fra circus
  firealarm(20);//sjekker om temp er høyere enn temperatur angitt i funksjons parameteret
  if(wake_up_value == 1){//sjekker om signal for stå opp lys er 1
    wake_up();//om lik 1, da vil stå opp lys være på, og kalle på funskjonen wake_up()
  }
  
  light();//kaller på funksjon light() som fungerer som en lysbryter
}

//FUNKSJONER
int getTemp(int tempPin){//returnerer temperatur
  int reading = analogRead(tempPin);//leser verdi fra temp sensor
  float voltage = reading/1025.0;// konverterer reading til spenning for 3.3v
  float temperature = (voltage - 0.5) * 100 ;  //konverterer til grader((spenning - 500mV)* 100)
  Serial.print(temperature); Serial.println(" degrees C");
  return temperature;
}

void setFan(){
  //JUSTERE VIFTE FREKVENS
  int vifte_value = circusESP32.read(key_fan,token);//leser verdi fra Circus
  //får inn verdi mellom 0-100 fra vifte_value
  vifte_value = map(vifte_value, 0,100 , 0, 510); //og gir ut tilsvarende verdi på intervallet 0-510
  digitalWrite(IN1, LOW);//IN1 og IN2 bestemmer retningen
  digitalWrite(IN2, HIGH);
  analogWrite(EN1,vifte_value);//får dc-motor til å snurre rundt
}
  
void setWindow(){
  //JUSTERE VINDU VINKEL
  int vindu_value = circusESP32.read(key_window,token);//Henter verdi fra signal vindu i circus
  myservo.write(vindu_value);//servo roterer mellom 0-50 grader, avhengig av circus
}

void setHeater(){
  //SKRU PÅ ELLER AV OVN AUTOMATISK
  int temp = getTemp(tempPin);//henter temperatur verdi fra funksjon
  int ovn_value = circusESP32.read(key_heater,token);// henter verdi fra circus
  if(temp< ovn_value){//ovn på/rød led på
    digitalWrite(heaterLed,HIGH);
  }else if(temp>= ovn_value){//ovn av/rød led av
    digitalWrite(heaterLed, LOW);
  }
}

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

void printLocalTime(){//printer klokkeslett nå (H:M:S)
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    Serial.println("Failed to obtain time");
    return;
  }
  Serial.println(&timeinfo, "%H:%M:%S");
 
}

void wake_up() { // "Lysalarm" kode, man velger selv hvilke klokkeslett lyset skal skru seg på og av
  time_t now = time(nullptr);
  struct tm* timeinfo = localtime(&now);
  printLocalTime(); //kaler funskjson som skriver til Seriell overvåker hva klokka er
   
  //verdier for time og minutter når lyset skal være på og av
  int hour_value_on = circusESP32.read(key_hour_on,token);
  int min_value_on = circusESP32.read(key_min_on,token);
  int hour_value_off = circusESP32.read(key_hour_off,token);
  int min_value_off = circusESP32.read(key_min_off,token);
  // TURN LED ON
  if( (timeinfo->tm_hour == hour_value_on) && (timeinfo->tm_min == min_value_on)){
      digitalWrite(roofLightLed,HIGH);
      circusESP32.write(key_LightSwitch, 1 ,token);//sender ON verdi til bryter 
  }
  // TURN LED OFF
  if( (timeinfo->tm_hour == hour_value_off) && (timeinfo->tm_min == min_value_off)){
      digitalWrite(roofLightLed,LOW);
      circusESP32.write(key_LightSwitch, 0 ,token);//sender OFF verdi til bryter
  }
  delay(1000);
}

void light() {// Her styres taklys gjennom CoT
  
  int light_value = circusESP32.read(key_LightSwitch,token);
  if (light_value == 1){
    digitalWrite(roofLightLed, HIGH); // Skru led på dersom knappen trykkes ON
  } 
  else{
    digitalWrite(roofLightLed, LOW);// Skru led av dersom knappen trykkes OFF
  }
}
