# SEGUNDO LABORATORIO DE SISTEMAS DIGITALES

**Elaborado por:** Kevin Tacha Herrera y Karol Rojas Gil 

**Dirigido a:** Diego Barragán 

**Guia Laboratorio:**[LABORATORIO II.pdf](https://github.com/user-attachments/files/27072427/LABORATORIO.II.pdf)


---

## Tabla de contenidos

- [Punto 1 — Sistema de Iluminación y Monitoreo de Temperatura](#punto-1--sistema-de-iluminación-y-monitoreo-de-temperatura)
- [Punto 2 — Juego en Pantalla OLED](#punto-2--juego-en-pantalla-oled)
- [Punto 3 — Detector de Colores con Sensor CNY70](#punto-3--detector-de-colores-con-sensor-cny70)

---

## Punto 1 - Sistema de Iluminación y Monitoreo de Temperatura

### ¿En qué consiste?

El objetivo de este punto fue construir un sistema capaz de controlar dos LEDs y leer la temperatura ambiente, todo manejado desde un chatbot conversacional que corre en la computadora. El usuario puede escribir o hablar por el chatbot, y el sistema responde encendiendo o apagando los LEDs, o reportando la temperatura medida por el sensor LM35 conectado al Arduino.

La comunicación entre la PC y el Arduino se hace a través del puerto serial (USB), usando Python con las librerías `pyserial` y `SpeechRecognition`.

### Materiales utilizados

- Arduino UNO
- Sensor de temperatura LM35
- LED Rojo + resistencia 220 ohm
- LED Verde + resistencia 220 ohm
- Protoboard y cables de conexión

### Conexión del circuito

| Componente | Pin Arduino |
|---|---|
| LM35 – VCC | 5V |
| LM35 – OUT | A0 |
| LM35 – GND | GND |
| LED Rojo (+ resistencia 220 ohm) | Pin 8 |
| LED Verde (+ resistencia 220 ohm) | Pin 9 |

### Evidencia fotografica:

<img width="1280" height="960" alt="img1 2" src="https://github.com/user-attachments/assets/18a3e25d-9fb0-4328-9175-de5462ca3d7a" />

<img width="1280" height="960" alt="img1 1" src="https://github.com/user-attachments/assets/64d47a56-eea1-4604-86e0-2f87f62ff2ea" />

https://github.com/user-attachments/assets/9242968a-0397-435d-aed2-0d6a3365dfe3


### Como funciona el código:

El sistema tiene dos archivos principales.

**`chatbot_arduino.ino`** - Se carga en el Arduino y queda escuchando comandos por el puerto serial. Cuando recibe `LED_ROJO_ON` enciende el LED rojo. Cuando recibe `TEMP`, lee el pin analógico A0, convierte el valor con la fórmula del LM35 (`voltaje / 10`) y devuelve la temperatura en grados Celsius.

**`chatbot.py`** - Corre en la computadora a traves dek PowerShell. Detecta automáticamente el puerto donde está el Arduino, interpreta el lenguaje natural del usuario (frases como "enciende el rojo" o "cuál es la temperatura") y envía el comando correspondiente al Arduino. También soporta entrada por voz usando el micrófono del computador.

### Comandos del chatbot:

| Lo que escribes o dices | Que pasa |
|---|---|
| `enciende el rojo` | LED rojo se enciende |
| `apaga el verde` | LED verde se apaga |
| `enciende las luces` | Ambos LEDs se encienden |
| `temperatura` | Reporta la temperatura actual |
| `voz` | Activa el micrófono |
| `ayuda` | Lista todos los comandos |
| `salir` | Cierra el programa |

### Como ejecutarlo:

```bash
# 1. Instalar dependencias
pip install pyserial SpeechRecognition pyaudio

# 2. Cargar chatbot_arduino.ino en el Arduino IDE

# 3. Ejecutar el chatbot
python chatbot.py
```

### Estructura de archivos

```
chatbot_krkt/
├── chatbot_arduino/
│   └── chatbot_arduino.ino
└── chatbot.py
```

---

## Punto 2 - Juego en Pantalla OLED

### ¿En qué consiste?

En este punto se desarrolló un videojuego funcional que corre en una pantalla OLED de 128x64 píxeles conectada al Arduino. El juego es un esquiva obstáculos: un personaje pixel-art corre automáticamente y el jugador debe hacerlo saltar para evitar los bloques que vienen desde la derecha. A medida que se acumulan puntos, el nivel sube y la velocidad aumenta.

Como no se contabamos con botones físicos, el control del juego se implementó desde la computadora usando el teclado, comunicándose con el Arduino por puerto serial igual que en el punto anterior.

### Materiales utilizados

- Arduino UNO
- Pantalla OLED 0.96 pulgadas 128x64 (controlador SSD1306, interfaz I2C)
- Cable USB (para conexión y control desde PC)
- Jumpers

### Conexión del circuito

| OLED | Arduino |
|---|---|
| VCC | 3.3V |
| GND | GND |
| SDA | A4 |
| SCL | A5 |

La pantalla OLED usa el protocolo I2C, que solo necesita dos cables de datos (SDA y SCL). La dirección I2C del módulo es `0x3C`, que es la más común. Si la pantalla no enciende se puede probar con `0x3D`.

### Evidencia fotografica

<img width="1179" height="902" alt="img2 1" src="https://github.com/user-attachments/assets/887e4000-ff65-46d6-9311-e4fcbd4711e3" />

https://github.com/user-attachments/assets/d6fd517f-17e6-4b21-b97b-8fdfb7ba031d

https://github.com/user-attachments/assets/f86c3f5f-1e46-481c-b435-ce9e8b6f0acb

### Como funciona el código

**`juego_oled.ino`** - Contiene toda la lógica del juego: física de salto con gravedad, generación aleatoria de obstáculos, detección de colisiones y renderizado frame a frame en la OLED. Escucha el puerto serial esperando el carácter `espacio` para saltar y `R`  para iniciar para reiniciar. El juego corre a aproximadamente 20 FPS usando `millis()` sin bloquear el procesador con `delay()`.

**`controlador.py`** - Corre en la computadora. Captura las teclas del teclado en tiempo real y las convierte en comandos seriales para el Arduino. También lee las respuestas del Arduino (puntos, nivel, game over) y las muestra en la terminal.

### Controles del juego

| Tecla | Accion |
|---|---|
| `ESPACIO` | Saltar |
| `R` | Reiniciar partida |
| `Q` | Cerrar el controlador |

### Librerias necesarias

Para el Arduino, instalar desde el Administrador de Bibliotecas del IDE:
- `Adafruit SSD1306`
- `Adafruit GFX Library`

Para Python:
```bash
pip install pyserial keyboard colorama
```

### Como ejecutarlo

```bash
# 1. Instalar dependencias Python
pip install pyserial keyboard colorama

# 2. Cargar juego_oled.ino en el Arduino IDE

# 3. Ejecutar el controlador (en Linux/Mac usar sudo)
python controlador.py
```

### Estructura de archivos

```
segundo_punto_krkt/
├── juego_oled/
│   └── juego_oled.ino
└── controlador.py
```

---

## Punto 3 - Detector de Colores con Sensor CNY70

### ¿En qué consiste?

Este punto consistió en construir un detector de superficies claras y oscuras usando el sensor óptico de reflexión CNY70. El sensor emite luz infrarroja y mide cuánta luz rebota de vuelta: las superficies blancas o claras reflejan mucha luz (señal alta), mientras que las negras u oscuras la absorben (señal baja). Con esto, el Arduino puede distinguir entre dos tipos de superficie y encender un LED indicador cuando detecta negro.

### Materiales utilizados

- Arduino UNO
- Sensor CNY70
- LED Rojo (indicador) + resistencia 220 ohm (R1)
- Resistencia 220 ohm para el emisor IR del CNY70 (R2)
- Resistencia 10k ohm para el receptor del CNY70 (R3)
- Protoboard y cables de conexión

### Conexión del circuito

| CNY70 (pin) | Conexion |
|---|---|
| Pin 1 — Anodo LED IR | 5V a traves de R2 (220 ohm) |
| Pin 2 — Catodo LED IR | GND |
| Pin 3 — Colector fototransistor | Pin 2 Arduino + R3 (10k ohm a 5V) |
| Pin 4 — Emisor fototransistor | GND |
| LED indicador (pata larga) | Pin 3 Arduino a traves de R1 (220 ohm) |
| LED indicador (pata corta) | GND |

Para identificar los pines del CNY70 hay que sostenerlo con la cara plana mirando hacia ti y los pines apuntando hacia abajo. De izquierda a derecha son: Pin 1, Pin 2, Pin 3, Pin 4. La resistencia R3 de 10k ohm es indispensable — sin ella la señal flota y el sensor da lecturas incorrectas. El CNY70 funciona mejor entre 0 y 5mm de la superficie.

### Evidencia fotografica

<img width="1280" height="960" alt="img3 1" src="https://github.com/user-attachments/assets/82e287f2-fb6b-4fd9-9fa0-598a33a8ce4e" />

<img width="1280" height="960" alt="img3 2" src="https://github.com/user-attachments/assets/090e2e84-6a7f-43b6-90c4-e6f6de26615e" />

<img width="1280" height="960" alt="img3 3" src="https://github.com/user-attachments/assets/aa42fbb3-dcea-432e-aa50-94a737695039" />

https://github.com/user-attachments/assets/1f57aea5-d28b-4311-bc01-a8d9091921a7

### Como funciona el código

**`detector_cny70.ino`** - Lee digitalmente el pin 2 cada 80-100ms. Si el valor es `0` (superficie oscura), enciende el LED y lo hace parpadear rápidamente para indicar detección activa. Si el valor es `1` (superficie clara), apaga el LED. Solo imprime por serial cuando el valor cambia, evitando saturar el monitor.

**`monitor_cny70.py`** - Monitor en Python que se conecta al Arduino por serial y muestra las detecciones en la terminal con colores. Al cerrar con Ctrl+C muestra un resumen con el conteo total de detecciones de cada tipo.

### Comportamiento del sistema

| Superficie | Señal del CNY70 | LED indicador | Serial |
|---|---|---|---|
| Blanca / Clara | HIGH (1) | Apagado | `BLANCO/CLARO detectado` |
| Negra / Oscura | LOW (0) | Parpadea | `NEGRO/OSCURO detectado` |

### Como ejecutarlo

```bash
# 1. Instalar dependencias
pip install pyserial colorama

# 2. Cargar detector_cny70.ino en el Arduino IDE

# 3. Ejecutar el monitor
python monitor_cny70.py
```

### Estructura de archivos

```
tercer_punto_krkt/
├── detector_cny70/
│   └── detector_cny70.ino
└── monitor_cny70.py
```

---

## Referencias

- [Arduino en la programacion y robotica educativa — UPM](https://blogs.upm.es/observatoriogate/2017/02/01/arduino-en-la-programacion-y-robotica-educativa/)
- [Sensor optico de reflexion CNY70 — Talos Electronics](https://www.taloselectronics.com/blogs/tutoriales/sensor-optico-de-reflexion-cny70)
- [Tutorial pantalla OLED con Arduino UNO — Solectroshop](https://solectroshop.com/es/content/47-tutorial-de-la-pantalla-oled-con-arduino-uno)

  










