#include "Keyboard.h"
#define BUTTON_COUNT 5

int button_states[BUTTON_COUNT];
int last_button_states[BUTTON_COUNT];
unsigned long last_debounce_time[BUTTON_COUNT];

unsigned long debounce_delay = 50;

void setup() {  
  Serial.begin(9600);
  // put your setup code here, to run once:  
  for(int i = 0; i < BUTTON_COUNT; i++) {
    pinMode(i +2, INPUT);
    last_button_states[i] = LOW;
  }
  
}

void loop() {  
  // put your main code here, to run repeatedly:
  for(int i = 0; i < BUTTON_COUNT; i++) 
    read_button(i);

   for(int i = 0; i < BUTTON_COUNT; i++) {
    Serial.print(button_states[i]);
    Serial.print(" "); 
   }
   Serial.print("\n");
    
  
}

void read_button(int i) {
  int reading = digitalRead(i + 2);

  if (reading != last_button_states[i])
    last_debounce_time[i] = millis();

   if((millis) - last_debounce_time[i] > debounce_delay) {
    if(reading != button_states[i]) {
      button_states[i] = reading;
    }
   }
}
