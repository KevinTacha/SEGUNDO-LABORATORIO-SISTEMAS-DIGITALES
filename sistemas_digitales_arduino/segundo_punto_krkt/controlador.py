import serial
import serial.tools.list_ports
import time
import sys
import threading

try:
    import keyboard
except ImportError:
    print("Falta la librería 'keyboard'. Instálala con:")
    print("   pip install keyboard")
    sys.exit(1)

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COL = True
except ImportError:
    COL = False

# ─────────────────────────────────────────────
BAUD_RATE = 9600

def color(txt, col):
    return (col + txt + Style.RESET_ALL) if COL else txt

def detectar_puerto():
    for p in serial.tools.list_ports.comports():
        if any(k in (p.description or "").upper()
               for k in ["ARDUINO","CH340","FTDI","USB SERIAL","ACM"]):
            return p.device
    puertos = serial.tools.list_ports.comports()
    return puertos[0].device if puertos else None

puntos_actuales = 0
nivel_actual    = 1
en_juego        = False
corriendo       = True

def leer_serial(arduino):
    global puntos_actuales, nivel_actual, en_juego, corriendo
    while corriendo:
        try:
            if arduino.in_waiting > 0:
                linea = arduino.readline().decode("utf-8", errors="ignore").strip()
                if not linea:
                    continue

                if linea == "LISTO":
                    print(color("\nArduino listo. Presiona ESPACIO para empezar.", Fore.CYAN))

                elif linea == "START":
                    en_juego = True
                    print(color("▶️   ¡Partida iniciada! ESPACIO = saltar  |  R = reiniciar  |  Q = salir", Fore.GREEN))

                elif linea == "SALTO":
                    print(color("¡Saltó!", Fore.YELLOW), end="\r")

                elif linea.startswith("PTS:"):
                    puntos_actuales = int(linea.split(":")[1])
                    print(color(f"  ★ Puntos: {puntos_actuales}  |  Nivel: {nivel_actual}", Fore.WHITE), end="\r")

                elif linea.startswith("NIV:"):
                    nivel_actual = int(linea.split(":")[1])
                    print(color(f"\n¡NIVEL {nivel_actual}! La velocidad aumentó.", Fore.MAGENTA))

                elif linea.startswith("GAMEOVER:"):
                    en_juego = False
                    partes   = linea.split(":")
                    pts = partes[1] if len(partes) > 1 else "?"
                    niv = partes[2] if len(partes) > 2 else "?"
                    print(color(f"\nGAME OVER - Puntos: {pts}  |  Nivel: {niv}", Fore.RED))
                    print(color("    Presiona ESPACIO o R para reiniciar.", Fore.YELLOW))

        except Exception:
            pass
        time.sleep(0.02)

def main():
    global corriendo

    puerto = detectar_puerto()
    if not puerto:
        print("No se encontró ningún Arduino conectado.")
        sys.exit(1)

    print(color(f"Arduino detectado en: {puerto}", Fore.GREEN))
    print("   Conectando...")

    try:
        arduino = serial.Serial(puerto, BAUD_RATE, timeout=1)
        time.sleep(2)
        arduino.reset_input_buffer()
    except serial.SerialException as e:
        print(f"Error al conectar: {e}")
        sys.exit(1)

    hilo = threading.Thread(target=leer_serial, args=(arduino,), daemon=True)
    hilo.start()

    print(color("\n" + "="*50, Fore.CYAN))
    print(color("CONTROLADOR - Esquiva Obstáculos OLED", Fore.CYAN))
    print(color("="*50, Fore.CYAN))
    print("  ESPACIO → Saltar")
    print("  R → Reiniciar")
    print("  Q → Salir\n")

    keyboard.add_hotkey('space', lambda: arduino.write(b'J'))  # Jump
    keyboard.add_hotkey('r',     lambda: arduino.write(b'S'))  # Start/Reset
    keyboard.add_hotkey('q',     lambda: salir(arduino))

    time.sleep(0.5)
    arduino.write(b'S')

    try:
        keyboard.wait('q')
    except KeyboardInterrupt:
        pass
    finally:
        salir(arduino)

def salir(arduino):
    global corriendo
    corriendo = False
    print(color("\n Cerrando controlador...", Fore.CYAN))
    try:
        arduino.close()
    except Exception:
        pass
    sys.exit(0)

if __name__ == "__main__":
    main()
