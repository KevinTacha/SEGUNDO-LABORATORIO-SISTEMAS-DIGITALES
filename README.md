# SEGUNDO LABORATORIO DE SISTEMAS DIGITALES

**Elaborado por:** Kevin Tacha Herrera y Karol Rojas Gil 

**Dirigido a:** Diego Barragán 

**Guia Taller:** [LABORATORIO II.pdf](https://github.com/user-attachments/files/27072358/LABORATORIO.II.pdf)


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

### EVIDENCIAS Y PRUEBAS REALES 

<img width="1280" height="960" alt="img1 2" src="https://github.com/user-attachments/assets/da22c866-1038-4642-935a-0931ebae9fa5" />

<img width="1280" height="960" alt="img1 1" src="https://github.com/user-attachments/assets/25d8d2bd-9984-492f-90a9-65fb5600df78" />

https://github.com/user-attachments/assets/7fbb8482-c0c5-40be-a2d0-fd26a09f299a

---

# SEGUNDO PUNTO

1. Descripción general
Creamos un juego minimalista pero funcional: “Catch the Pixel” (Atrapa el píxel). En la pantalla OLED aparece un punto que se mueve aleatoriamente y el jugador debe seguir su posición con un cursor controlado por dos botones (izquierda/derecha o arriba/abajo, según el diseño). Cada vez que el cursor coincide con el punto, se suma un punto, el punto cambia de posición y la puntuación se actualiza en pantalla. El juego incluye un contador de tiempo o de vidas (opcional) para darle emoción.

2. Componentes utilizados
Placa Arduino UNO (también válido para Nano o Mega).

Pantalla OLED de 0.96″ o 1.3″ con controlador SSD1306 (comunicación I2C).

Dos pulsadores (botones) con resistencias pull-down de 10kΩ (o usando pull-up internos).

Protoboard y cables jumper.

3. Conexiones (hardware)
Componente	Pin Arduino
OLED VCC	5V
OLED GND	GND
OLED SCL	A5 (o pin SCL)
OLED SDA	A4 (o pin SDA)

4. Librerías necesarias para Arduino
Instalamos las siguientes librerías desde el Gestor de Librerías del IDE de Arduino:

Adafruit SSD1306 (para controlar la OLED)

Adafruit GFX (gráficos básicos)

5. Código de Arduino (juego)
El programa dibuja un cursor (cuadrado de 8x8 píxeles) y un objetivo (círculo de 4x4). Los botones mueven el cursor en el eje X (o Y). Al solapar cursor y objetivo, se incrementa la puntuación, el objetivo se reposiciona aleatoriamente y se reproduce un tono.

### CODIGO

6. Procedimiento paso a paso
Montaje físico: Seguimos el esquema de conexiones, verificando que la OLED aparezca en la dirección I2C correcta (usamos un escáner I2C si es necesario).

Instalación de librerías: Desde el IDE de Arduino, instalamos Adafruit SSD1306 y Adafruit GFX.

Carga del código: Copiamos el código, ajustamos pines si es necesario y lo cargamos en la Arduino UNO.

Prueba inicial: Al encender, la OLED muestra un cursor y un objetivo. Los botones mueven el cursor horizontalmente.

Ajustes de jugabilidad: Modificamos el intervalo de movimiento y el tamaño de los objetos para que sea desafiante pero jugable.

Opcionales: Añadimos un buzzer para feedback auditivo, un límite de tiempo o un sistema de vidas.

7. Documentación en GitHub
Creamos un repositorio público llamado arduino-oled-game que contiene:

README.md:

Explicación del juego, reglas y materiales.

Diagrama de conexiones (imagen Fritzing o foto clara).

Instrucciones de instalación de librerías y carga del código.

Gif o video corto mostrando el juego en funcionamiento.

Carpeta /code:

oled_game.ino (código principal).

I2C_scanner.ino (utilidad opcional para comprobar la dirección de la OLED).

Carpeta /images:

Foto del montaje.

Esquema eléctrico.

Sección de “Mejoras futuras”:

Añadir más botones para mover también en Y.

Guardar puntuación más alta en EEPROM.

Niveles de dificultad creciente.

### EVIDENCIAS Y PRUEBAS REALES


<img width="1179" height="902" alt="img2 1" src="https://github.com/user-attachments/assets/b9faec61-3c66-45ca-aedf-66e2adcc3b05" />

https://github.com/user-attachments/assets/6ab8eaaa-bbc2-4009-9f08-0360e561067a

https://github.com/user-attachments/assets/ebeb7f8d-e3b9-40ac-b69b-ee759f434826












