#include <JC_Button.h>
#include <Arduino_FreeRTOS.h>

#define STEPPER

#ifdef STEPPER
#include <TinyStepper_28BYJ_48.h>

byte MOTOR_IN1_PIN = 7;
byte MOTOR_IN2_PIN = 6;
byte MOTOR_IN3_PIN = 5;
byte MOTOR_IN4_PIN = 4;
const int16_t STEPS_PER_REVOLUTION = 2048;
TinyStepper_28BYJ_48 stepper;
#endif

byte irPin = 3;
Button myButton(irPin, 120, false, false);
uint32_t count = 0;
volatile bool countFlag = false;
volatile uint8_t seeds_to_dispense = 0;


void contadorSemilla(void * param){
  for(;;){
    // Serial.println("JHola");
    myButton.read();
    if(countFlag && myButton.wasPressed()){
      seeds_to_dispense--;
      Serial.print("Semillas restantes: ");
      Serial.println(seeds_to_dispense);
      if(seeds_to_dispense == 0) countFlag = false;

    }
  }
}

void listenSerial(void * param){
  for(;;){
    if (Serial.available())
    {
      String valor = Serial.readString();

      if(valor.startsWith("stop")){
        countFlag = false;
        // count = 0;
        Serial.println("Ha detenido!");
      }

      else if(valor.startsWith("seeds:")){
        countFlag = true;
        count = 0;
        seeds_to_dispense = (uint8_t) valor.substring(6, valor.length()).toInt();
        Serial.print("Se dosificará ");
        Serial.println(seeds_to_dispense);
      }
      else {
        Serial.print("Se recibió: ");
        Serial.println(valor);
      }
    }
  }
}

void desplazarMotor (void * param){
  for(;;){
    // Serial.println("Vemçamo");
    if(countFlag && seeds_to_dispense > 0){
      Serial.println("Moviendo motor");
      #ifdef STEPPER
      stepper.moveRelativeInSteps(342);
      #endif
    }
  }
}

void setup(){
  Serial.begin(9600);
  Serial.println("Starting");
  // pinMode(LED_BUILTIN, OUTPUT);
  // digitalWrite(LED_BUILTIN, LOW);
  myButton.begin();

  #ifdef STEPPER
  stepper.connectToPins(MOTOR_IN1_PIN, MOTOR_IN2_PIN, MOTOR_IN3_PIN, MOTOR_IN4_PIN);
  stepper.setSpeedInStepsPerSecond(15);
  stepper.setAccelerationInStepsPerSecondPerSecond(200);
  // stepper.setCurrentPositionInSteps(0);
  #endif

  xTaskCreate(
    contadorSemilla
    ,  "contadorSemilla"        // Nombre descriptivo de la función (MAX 8 caracteres)
    ,  128               // Tamaño necesario en memoria STACK
    ,  NULL              // Parámetro INICIAL a recibir
    ,  1                 // Prioridad, prioridad = 3 (configMAX_PRIORITIES - 1) es la mayor, prioridad = 0 es la menor.
    ,  NULL );           // Variable que apunta al task (opcional)
  
  xTaskCreate(
    listenSerial
    ,  "listenSerial"        // Nombre descriptivo de la función (MAX 8 caracteres)
    ,  128               // Tamaño necesario en memoria STACK
    ,  NULL              // Parámetro INICIAL a recibir
    ,  1                 // Prioridad, prioridad = 3 (configMAX_PRIORITIES - 1) es la mayor, prioridad = 0 es la menor.
    ,  NULL );           // Variable que apunta al task (opcional)
  
  xTaskCreate(
    desplazarMotor
    ,  "contadorSemilla"        // Nombre descriptivo de la función (MAX 8 caracteres)
    ,  128               // Tamaño necesario en memoria STACK
    ,  NULL              // Parámetro INICIAL a recibir
    ,  1                 // Prioridad, prioridad = 3 (configMAX_PRIORITIES - 1) es la mayor, prioridad = 0 es la menor.
    ,  NULL );           // Variable que apunta al task (opcional)
}

void loop(){

}