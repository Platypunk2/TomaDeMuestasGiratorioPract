#define DIR_PIN 2
#define STEP_PIN 3
#define MS1_PIN 7
#define MS2_PIN 4
#define SLEEP_PIN 8

#define DIR_PIN2 11
#define STEP_PIN2 10
#define MS1_PIN2 6
#define MS2_PIN2 9
#define SLEEP_PIN2 5

#define STEP_PIN_GIRO 12
#define DIR_PIN_GIRO 13

String final="", inf = "1.8", sup = "360";  
char ascii;
float nogrados;
float movimiento = 0;
bool valid = false;

void setup() {
  pinMode(DIR_PIN, OUTPUT); 
  pinMode(STEP_PIN, OUTPUT); 
  pinMode(DIR_PIN2, OUTPUT); 
  pinMode(STEP_PIN2, OUTPUT); 
  pinMode(STEP_PIN_GIRO, OUTPUT);
  pinMode(DIR_PIN_GIRO, OUTPUT);
  Serial.begin(115200);

}

void loop() {
  if(Serial.available()){
      char ascii=Serial.read();
      char c=ascii;

      switch(c){
        case 'G':
          rotateDegMotor3(360, .23); //BY ERICK .05 , .1 es el maximo soportado, cuando todo esta armado encima del brazo: vubiq+ placa baseband+cables = 2.4 s la vuelta completa
          //rotate(-1600, .25); //reverse
          Serial.println("OK");
          break;
          
        case 'H':
          rotateDegMotor3(-360, .23); // BY ERICK .05 
          //rotate(-1600, .25); //reverse
          Serial.println("OK");
          break;
          
        case 'N': 
          while(movimiento<inf.toFloat() || movimiento >sup.toFloat()){
            if(Serial.available()>0 && !valid){
              ascii = Serial.read();
              if(ascii=='\r'){
                movimiento = (final.toFloat());
                valid=true;
              }
              final += ascii;
            }
            
            
          }
          nogrados=(final.toFloat()); 
          rotateDegMotor3(nogrados, .35); // BY ERICK .05// .23 albert=2.08s/vuelta--> 60vueltas=3min42seg=222seg,(con script matplotlib y placa acoplada al brazo)... //.35 con placa desacoplada del brazo -->1.38 s/vuelta  --> 60 vueltas=2min38seg = 158seg (con el script de matplotlib)
          //rotate(-1600, .25); //reverse
          Serial.println("O");
          final = "";
        // yes: convert to integer and add to “final”.
          movimiento = 0;
          valid =false;
          break;
          
        case 'O':
          while(movimiento<inf.toFloat() || movimiento >sup.toFloat()){
            if(Serial.available()>0 && !valid){
              ascii = Serial.read();
              if(ascii=='\r'){
                movimiento = (final.toFloat());
                valid=true;
              }
              final += ascii;
            }
          }
          nogrados=(final.toFloat());
          rotateDegMotor3(-nogrados, .35); // BY ERICK .05 , .23 albert
          //rotate(-1600, .25); //reverse
          Serial.println("O");
          final = "";
          // yes: convert to integer and add to “final”.
          movimiento = 0;
          valid = false;
          break;

          case 'E':
            rotateDegMotor3(1.8, .1); 
            Serial.println("OK");
            break;

          case 'F':
            rotateDegMotor3(-1.8, .1); 
            Serial.println("OK");
            break;
      }
      
  }

}
void rotate(int steps, float speed){ 
  //rotate a specific number of microsteps (8 microsteps per step) - (negitive for reverse movement)
  //speed is any number from .01 -> 1 with 1 being fastest - Slower is stronger
  int dir = (steps > 0)? HIGH:LOW;
  steps = abs(steps);

  digitalWrite(DIR_PIN_GIRO,dir); 

  float usDelay = (1/speed) * 70;

  for(int i=0; i < steps; i++){ 
    digitalWrite(STEP_PIN_GIRO, HIGH); 
    delayMicroseconds(usDelay); 

    digitalWrite(STEP_PIN_GIRO, LOW); 
    delayMicroseconds(usDelay); 
  } 
} 

void rotateDegMotor1(float deg, float speed){ 
  //rotate a specific number of degrees (negitive for reverse movement)
  //speed is any number from .01 -> 1 with 1 being fastest - Slower is stronger
  int dir = (deg > 0)? HIGH:LOW;
  digitalWrite(DIR_PIN,dir); 

  int steps = abs(deg)*(1/0.225);
  float usDelay = (1/speed) * 70;

  for(int i=0; i < steps; i++){ 
    digitalWrite(STEP_PIN, HIGH); 
    delayMicroseconds(usDelay); 

    digitalWrite(STEP_PIN, LOW); 
    delayMicroseconds(usDelay); 
  } 
}

void rotateDegMotor2(float deg, float speed){ 
  //rotate a specific number of degrees (negitive for reverse movement)
  //speed is any number from .01 -> 1 with 1 being fastest - Slower is stronger
  int dir = (deg > 0)? HIGH:LOW;
  digitalWrite(DIR_PIN2,dir); 

  int steps = abs(deg)*(1/0.225);
  float usDelay = (1/speed) * 70;

  for(int i=0; i < steps; i++){ 
    digitalWrite(STEP_PIN2, HIGH); 
    delayMicroseconds(usDelay); 

    digitalWrite(STEP_PIN2, LOW); 
    delayMicroseconds(usDelay); 
  } 
}




void rotateDegMotor3(float deg, float speed){ 
  //rotate a specific number of degrees (negitive for reverse movement)
  //speed is any number from .01 -> 1 with 1 being fastest - Slower is stronger
  int dir = (deg > 0)? HIGH:LOW;
  digitalWrite(DIR_PIN_GIRO,dir); 

  int steps = abs(deg)*(1/0.1125);
  float usDelay = (1/speed) * 70;

  for(int i=0; i < steps; i++){ 
    digitalWrite(STEP_PIN_GIRO, HIGH); 
    delayMicroseconds(usDelay); 

    digitalWrite(STEP_PIN_GIRO, LOW); 
    delayMicroseconds(usDelay); 
  } 
}
