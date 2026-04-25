# SEGUNDO LABORATORIO DE SISTEMAS DIGITALES

**Elaborado por:** Kevin Tacha Herrera y Karol Rojas Gil 

**Dirigido a:** Diego Barragán 

---

### PRIMER PUNTO ### 

1. Componentes y conexiones (hardware)
Utilizamos una placa Arduino UNO, un sensor LM35 (temperatura), dos LEDs (rojo y verde) con resistencias de 220 Ω y una protoboard.

Conexiones realizadas:

LED rojo: ánodo al pin digital 9, cátodo a GND mediante resistencia de 220 Ω.

LED verde: ánodo al pin digital 10, cátodo a GND mediante resistencia de 220 Ω.

LM35: pin VCC a 5V de Arduino, GND a GND, salida (OUT) al pin analógico A0.

Montamos todos los componentes en la protoboard y usamos cables jumper para las conexiones.

2. Código de Arduino
El programa que cargamos en Arduino lee la temperatura del LM35, recibe comandos por el puerto serie y actúa sobre los LEDs. También envía la temperatura medida cuando se le solicita.

# IMAGEN CODIGO

3. Chatbot en Python (PC)
En la computadora desarrollamos un chatbot que acepta entrada por texto o voz, se comunica por serial con Arduino y responde al usuario. Usamos las librerías pyserial, speech_recognition y pyttsx3

 # IMAGEN CODIGO

 4. Funcionamiento integrado
Conexión: Conectamos Arduino por USB y cerramos el IDE para que Python pueda acceder al puerto.

Ejecución: Corremos python chatbot_serial.py en la terminal.

Interacción:

Si escribimos encender rojo → Arduino enciende el LED rojo y responde "LED rojo encendido".

Si escribimos temperatura → Arduino lee el LM35 y envía algo como "Temperatura: 25.3 °C".

Si escribimos voz → el programa activa el micrófono, convierte nuestra voz a texto y lo envía como comando.

Validación: Probamos todas las combinaciones (encender/apagar cada LED, consulta de temperatura, comandos inválidos). El chatbot respondió correctamente en todos los casos.
