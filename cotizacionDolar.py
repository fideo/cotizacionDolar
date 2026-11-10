import os
import sys
import time

import requests
from bs4 import BeautifulSoup

ES_WINDOWS = sys.platform == "win32"

# Carpeta del script (o del ejecutable si está empaquetado con PyInstaller)
BASE_DIR = (
    os.path.dirname(sys.executable)
    if getattr(sys, "frozen", False)
    else os.path.dirname(os.path.abspath(__file__))
)
PATH_ESTADO = os.path.join(BASE_DIR, "cotizacion.txt")
# .ico para Windows; en Linux conviene un .png (ej: iconoDolar.png)
PATH_ICONO = os.path.join(BASE_DIR, "iconoDolar.ico" if ES_WINDOWS else "iconoDolar.png")


def notificar(titulo, mensaje):
    try:
        if ES_WINDOWS:
            from windows_toasts import (
                InteractableWindowsToaster, Toast, ToastDisplayImage,
            )
            toaster = InteractableWindowsToaster("Cotizador Dólar BNA")
            toast = Toast()
            toast.text_fields = [titulo, mensaje]
            if os.path.exists(PATH_ICONO):
                toast.AddImage(ToastDisplayImage.fromPath(PATH_ICONO))
            toaster.show_toast(toast)
        else:
            from plyer import notification
            notification.notify(
                title=titulo,
                message=mensaje,
                app_name="Cotizador Dólar BNA",
                app_icon=PATH_ICONO if os.path.exists(PATH_ICONO) else "",
                timeout=10,
            )
        time.sleep(1)
    except Exception as e:
        # Así, si falla el popup, queda registrado en el log de cron/systemd
        print(f"No se pudo mostrar la notificación: {e}", file=sys.stderr)


# --- Obtención de datos ---
r = requests.get("https://www.bna.com.ar/Personas", timeout=15)
soup = BeautifulSoup(r.text, "html.parser")

tabla_dolar = soup.find("table", class_="table cotizacion")
tabla_hora = soup.find("div", class_="legal")

dolar_formateado = tabla_dolar.find_all("td")[2].get_text(strip=True)[0:6]
hora_actual = tabla_hora.text[20:25]

print(dolar_formateado, "- Hora act.", hora_actual)

# --- Estado anterior ---
valor_anterior, hora_anterior = "", ""
if os.path.exists(PATH_ESTADO):
    with open(PATH_ESTADO, "r", encoding="utf-8") as f:
        contenido = f.read(17).strip("\n")
    valor_anterior = contenido[0:6]
    hora_anterior = contenido[12:17]

print(valor_anterior, "-", dolar_formateado)
print(hora_anterior, "-", hora_actual)

hubo_cambio_valor = valor_anterior != dolar_formateado
hubo_cambio_hora = hora_anterior != hora_actual

# --- Notificación si hubo cambios ---
if hubo_cambio_valor or hubo_cambio_hora:
    if hubo_cambio_valor:
        titulo = "CAMBIÓ LA COTIZACIÓN DEL DÓLAR"
        mensaje = f"Nuevo valor: ${dolar_formateado} (Hora: {hora_actual})"
    else:
        titulo = "ACTUALIZACIÓN DE HORARIO DÓLAR"
        mensaje = f"Valor actual: ${dolar_formateado} (Nueva Hora: {hora_actual})"
    notificar(titulo, mensaje)

# --- Guardar estado actual (sobrescribe todo el archivo) ---
with open(PATH_ESTADO, "w", encoding="utf-8") as f:
    f.write(f"{dolar_formateado} Hora {hora_actual}")