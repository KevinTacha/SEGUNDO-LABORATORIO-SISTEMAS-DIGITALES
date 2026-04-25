import serial
import serial.tools.list_ports
import time
import sys
from datetime import datetime

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR_DISPONIBLE = True
except ImportError:
    COLOR_DISPONIBLE = False
    print("[INFO] Instala 'colorama' para ver colores: pip install colorama")

BAUD_RATE   = 9600
TIMEOUT_SER = 2


def txt_negro(msg):
    if COLOR_DISPONIBLE:
        return Fore.WHITE + Style.BRIGHT + "Negro " + msg + Style.RESET_ALL
    return "[NEGRO] " + msg

def txt_blanco(msg):
    if COLOR_DISPONIBLE:
        return Fore.YELLOW + Style.BRIGHT + "Blanco" + msg + Style.RESET_ALL
    return "[BLANCO] " + msg

def txt_info(msg):
    if COLOR_DISPONIBLE:
        return Fore.CYAN + msg + Style.RESET_ALL
    return msg

def detectar_puerto():
    puertos = serial.tools.list_ports.comports()
    for p in puertos:
        if any(kw in (p.description or "").upper()
               for kw in ["ARDUINO", "CH340", "FTDI", "USB SERIAL", "ACM"]):
            return p.device
    if puertos:
        return puertos[0].device
    return None

def iniciar_monitor(arduino: serial.Serial):
    print(txt_info("\n" + "="*50))
    print(txt_info("   DETECTOR DE COLORES MEDIANTE SENSOR CNY70"))
    print(txt_info("   Creado por: Kevin Tacha y Karol Rojas "))
    print(txt_info("   Puerto: " + arduino.port))
    print(txt_info("   Presiona Ctrl+C para salir"))
    print(txt_info("="*50 + "\n"))

    conteo = {"negro": 0, "blanco": 0}

    try:
        while True:
            if arduino.in_waiting > 0:
                linea = arduino.readline().decode("utf-8", errors="ignore").strip()

                if not linea:
                    continue

                hora = datetime.now().strftime("%H:%M:%S")

                if "NEGRO" in linea.upper() or "OSCURO" in linea.upper():
                    conteo["negro"] += 1
                    print(f"[{hora}] {txt_negro('Superficie NEGRA o OSCURA detectada')}")

                elif "BLANCO" in linea.upper() or "CLARO" in linea.upper():
                    conteo["blanco"] += 1
                    print(f"[{hora}] {txt_blanco('Superficie BLANCA o CLARA detectada')}")

                else:
                    print(txt_info(f"[{hora}] {linea}"))

            time.sleep(0.05)

    except KeyboardInterrupt:
        print(txt_info("\n\n--- Sesión finalizada ---"))
        print(txt_info(f"  Detecciones negras:  {conteo['negro']}"))
        print(txt_info(f"  Detecciones blancas: {conteo['blanco']}"))
        total = conteo['negro'] + conteo['blanco']
        if total > 0:
            pct_n = conteo['negro']  * 100 // total
            pct_b = conteo['blanco'] * 100 // total
            print(txt_info(f"  Negro: {pct_n}%  |  Blanco: {pct_b}%"))
        print()
def main():
    puerto = detectar_puerto()

    if puerto is None:
        print("No se encontró ningún Arduino conectado.")
        print("   Verifica la conexión USB e intenta de nuevo.")
        sys.exit(1)

    print(f"Arduino detectado en: {puerto}")
    print("   Conectando...")

    try:
        arduino = serial.Serial(puerto, BAUD_RATE, timeout=TIMEOUT_SER)
        time.sleep(2)  
        arduino.reset_input_buffer()
        iniciar_monitor(arduino)

    except serial.SerialException as e:
        print(f"Error al abrir el puerto {puerto}: {e}")
        sys.exit(1)
    finally:
        if 'arduino' in locals() and arduino.is_open:
            arduino.close()
            print("Puerto serial cerrado.")

if __name__ == "__main__":
    main()
