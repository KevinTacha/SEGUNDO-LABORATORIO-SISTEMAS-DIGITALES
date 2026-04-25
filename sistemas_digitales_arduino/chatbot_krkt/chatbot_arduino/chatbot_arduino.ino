const int PIN_LED_ROJO  = 8;
const int PIN_LED_VERDE = 9;
const int PIN_LM35      = A0;

void setup() {
  Serial.begin(9600);
  pinMode(PIN_LED_ROJO,  OUTPUT);
  pinMode(PIN_LED_VERDE, OUTPUT);
  digitalWrite(PIN_LED_ROJO,  LOW);
  digitalWrite(PIN_LED_VERDE, LOW);
  Serial.println("ARDUINO_LISTO");
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "LED_ROJO_ON") {
      digitalWrite(PIN_LED_ROJO, HIGH);
      Serial.println("LED_ROJO_ENCENDIDO");

    } else if (cmd == "LED_ROJO_OFF") {
      digitalWrite(PIN_LED_ROJO, LOW);
      Serial.println("LED_ROJO_APAGADO");

    } else if (cmd == "LED_VERDE_ON") {
      digitalWrite(PIN_LED_VERDE, HIGH);
      Serial.println("LED_VERDE_ENCENDIDO");

    } else if (cmd == "LED_VERDE_OFF") {
      digitalWrite(PIN_LED_VERDE, LOW);
      Serial.println("LED_VERDE_APAGADO");

    } else if (cmd == "LEDS_ON") {
      digitalWrite(PIN_LED_ROJO,  HIGH);
      digitalWrite(PIN_LED_VERDE, HIGH);
      Serial.println("AMBOS_LEDS_ENCENDIDOS");

    } else if (cmd == "LEDS_OFF") {
      digitalWrite(PIN_LED_ROJO,  LOW);
      digitalWrite(PIN_LED_VERDE, LOW);
      Serial.println("AMBOS_LEDS_APAGADOS");

    } else if (cmd == "TEMP") {
      int lectura   = analogRead(PIN_LM35);
      float voltaje = lectura * (5000.0 / 1023.0);   
      float temp    = voltaje / 10.0;                 
      Serial.print("TEMPERATURA:");
      Serial.println(temp, 1);                       

    } else {
      Serial.println("CMD_DESCONOCIDO");
    }
  }
}
