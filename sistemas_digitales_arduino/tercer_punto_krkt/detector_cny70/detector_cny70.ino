
const int PIN_SENSOR = 2;   
const int PIN_LED    = 3; 

int valorSensor   = 0;
int lecturaAnterior = -1; 
int contadorNegro = 0;
int contadorBlanco = 0;

void setup() {
  Serial.begin(9600);
  pinMode(PIN_SENSOR, INPUT);
  pinMode(PIN_LED,    OUTPUT);
  digitalWrite(PIN_LED, LOW);

  Serial.println("=====================================");
  Serial.println("  Detector de Color realizado por Kevin Tacha y Karol Rojas");
  Serial.println("  Acerca el sensor al color.");
  Serial.println("=====================================");
}

void loop() {
  valorSensor = digitalRead(PIN_SENSOR);
  delay(100);

  if (valorSensor != lecturaAnterior) {

    if (valorSensor == 0) {
      contadorNegro++;
      Serial.print(">> COLOR DETECTADO: NEGRO/OSCURO  ");
      Serial.print("| Total negros: ");
      Serial.println(contadorNegro);
      digitalWrite(PIN_LED, HIGH);  

    } else {
      contadorBlanco++;
      Serial.print(">> COLOR DETECTADO: BLANCO/CLARO  ");
      Serial.print("| Total blancos: ");
      Serial.println(contadorBlanco);
      digitalWrite(PIN_LED, LOW); 
    }
    lecturaAnterior = valorSensor;
  }
}
