import serial
import serial.tools.list_ports
import speech_recognition as sr
import time
import sys
import threading

BAUD_RATE    = 9600
TIMEOUT_SER  = 2          
IDIOMA_VOZ   = "es-ES"    

def detectar_puerto_arduino():
    """Detecta automaticamente el puerto donde esta conectado el Arduino."""
    puertos = serial.tools.list_ports.comports()
    for p in puertos:
        if any(kw in (p.description or "").upper()
               for kw in ["ARDUINO", "CH340", "FTDI", "USB SERIAL", "ACM"]):
            return p.device
    # Fallback: primer puerto disponible
    if puertos:
        return puertos[0].device
    return None

def enviar_comando(arduino: serial.Serial, comando: str) -> str:
    """Envia un comando al Arduino y retorna la respuesta."""
    try:
        arduino.write((comando + "\n").encode("utf-8"))
        time.sleep(0.1)
        respuesta = arduino.readline().decode("utf-8").strip()
        return respuesta
    except serial.SerialException as e:
        return f"ERROR_SERIAL: {e}"

def interpretar_mensaje(texto: str):
    """
    Analiza el mensaje del usuario y retorna una tupla
    (comando_arduino, respuesta_chatbot).
    Si no se necesita comando devuelve (None, respuesta).
    """
    t = texto.lower().strip()

    if any(p in t for p in ["temperatura", "temp", "calor", "frio", "grados",
                              "cuanto mide", "que temperatura"]):
        return ("TEMP", None)  

    if any(p in t for p in ["enciende el rojo", "encender rojo", "led rojo on",
                              "prende el rojo", "prender rojo"]):
        return ("LED_ROJO_ON",
                "Entendido! Encendiendo el LED rojo.")

    if any(p in t for p in ["apaga el rojo", "apagar rojo", "led rojo off",
                              "apaga rojo"]):
        return ("LED_ROJO_OFF",
                "Apagando el LED rojo.")

    if any(p in t for p in ["enciende el verde", "encender verde", "led verde on",
                              "prende el verde", "prender verde"]):
        return ("LED_VERDE_ON",
                "Entendido! Encendiendo el LED verde.")

    if any(p in t for p in ["apaga el verde", "apagar verde", "led verde off",
                              "apaga verde"]):
        return ("LED_VERDE_OFF",
                "Apagando el LED verde.")

    if any(p in t for p in ["enciende todo", "encender todo", "enciende los leds",
                              "encender leds", "prende todo", "encender las luces",
                              "enciende las luces", "luces on"]):
        return ("LEDS_ON",
                "Encendiendo ambos LEDs!")

    if any(p in t for p in ["apaga todo", "apagar todo", "apaga los leds",
                              "apagar leds", "apaga las luces", "luces off",
                              "apagar las luces"]):
        return ("LEDS_OFF",
                "Apagando todos los LEDs.")

    if any(p in t for p in ["hola", "buenos dias", "buenas tardes", "buenas noches",
                              "hey", "hi"]):
        return (None,
                "Hola! Soy un chat bot creado por Kevin Tacha y Karol Rojas y sere tu asistente de iluminacion y temperatura."
                "Que quieres hacer hoy?")

    if any(p in t for p in ["ayuda", "help", "que puedes hacer", "que puedes hacer",
                              "comandos", "opciones"]):
        return (None,
                "Puedo hacer lo siguiente:\n"
                "  - 'Enciende el LED rojo / verde'\n"
                "  - 'Apaga el LED rojo / verde'\n"
                "  - 'Enciende las luces' / 'Apaga las luces'\n"
                "  - 'Cual es la temperatura?'\n"
                "  - Escribe 'voz' para hablarme\n"
                "  - Escribe 'salir' para terminar")
    
    if any(p in t for p in ["adios", "adios", "bye", "salir", "hasta luego",
                              "chao", "chau"]):
        return ("SALIR", "Hasta luego! Apagando los LEDs...")

    return (None,
            "No entendi eso. Escribe 'ayuda' para ver qué puedo hacer.")

def escuchar_voz() -> str:
    """Captura audio del microfono y retorna el texto reconocido."""
    recognizer = sr.Recognizer()
    mic         = sr.Microphone()

    print("Escuchando... (habla ahora)")
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        texto = recognizer.recognize_google(audio, language=IDIOMA_VOZ)
        print(f"Escuche: '{texto}'")
        return texto

    except sr.WaitTimeoutError:
        return "__TIMEOUT__"
    except sr.UnknownValueError:
        return "__NO_ENTENDIDO__"
    except sr.RequestError as e:
        return f"__ERROR_API__: {e}"


def iniciar_chatbot(arduino: serial.Serial):
    print("\n" + "="*55)
    print("CHATBOT - Iluminación y Temperatura")
    print("      Arduino conectado en:", arduino.port)
    print("="*55)
    print("  Escribe tu mensaje o 'voz' para usar el micrófono.")
    print("  Escribe 'salir' o 'adios' para terminar.\n")

    while True:
        try:
            entrada = input("Tu: ").strip()
        except (KeyboardInterrupt, EOFError):
            entrada = "salir"

        if not entrada:
            continue

        if entrada.lower() == "voz":
            resultado_voz = escuchar_voz()
            if resultado_voz == "__TIMEOUT__":
                print("Bot: No detecte ninguna voz. Intentalo de nuevo.\n")
                continue
            elif resultado_voz == "__NO_ENTENDIDO__":
                print("Bot: No pude entender lo que dijiste. Puedes repetir?\n")
                continue
            elif resultado_voz.startswith("__ERROR_API__"):
                print(f"Bot: Error de reconocimiento: {resultado_voz}\n")
                continue
            else:
                entrada = resultado_voz 
        comando, respuesta = interpretar_mensaje(entrada)

        if comando == "SALIR":
            print(f"Bot: {respuesta}")
            enviar_comando(arduino, "LEDS_OFF")
            print("     Conexion cerrada. Hasta pronto!\n")
            break

        if comando:
            eco_arduino = enviar_comando(arduino, comando)

            if comando == "TEMP":
                if eco_arduino.startswith("TEMPERATURA:"):
                    valor = eco_arduino.split(":")[1]
                    respuesta = (f"La temperatura actual es de "
                                 f"{valor} °C.")
                else:
                    respuesta = (f"No pude leer la temperatura. "
                                 f"(Arduino: {eco_arduino})")

        print(f"Bot: {respuesta}\n")


def main():
    puerto = detectar_puerto_arduino()

    if puerto is None:
        print("No se encontro ningun Arduino conectado.")
        print("   Verifica la conexion USB y vuelve a intentar.")
        sys.exit(1)

    print(f"Arduino detectado en: {puerto}")
    print("    Esperando inicializacion del Arduino...")

    try:
        arduino = serial.Serial(puerto, BAUD_RATE, timeout=TIMEOUT_SER)
        time.sleep(2)    

        inicio = time.time()
        while time.time() - inicio < 5:
            linea = arduino.readline().decode("utf-8").strip()
            if linea == "ARDUINO_LISTO":
                print("Arduino listo.\n")
                break
        else:
            print("El Arduino no respondio 'ARDUINO_LISTO'. Continuando...")

        iniciar_chatbot(arduino)

    except serial.SerialException as e:
        print(f"Error al abrir el puerto {puerto}: {e}")
        sys.exit(1)
    finally:
        if 'arduino' in locals() and arduino.is_open:
            arduino.close()
            print("Puerto serial cerrado.")


if __name__ == "__main__":
    main()
