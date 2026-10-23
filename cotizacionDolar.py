import time
import requests
import os
import sys
from bs4 import BeautifulSoup
#from plyer import notification
from windows_toasts import InteractableWindowsToaster, Toast

# Obtengo la url del sitio a obtener los datos
url = 'https://www.bna.com.ar/Personas'

# A través de request obtengo todo el código de la url pasada
r = requests.get(url)

# Paso a BeautifulSoup lo obtenido como texto y lo parseo como HTML
soup = BeautifulSoup(r.text, 'html.parser')

# Busco el tag table con class table cotización
tabla_dolar = soup.find('table', class_='table cotizacion')
tabla_hora = soup.find('div', class_='legal')

dolar = 0

# Recorro la tabla encontrando los tags tbody
for cotizacion in tabla_dolar.find_all('td')[2]:
    # dolar = cotizacion.find_all('td')[2].text
    dolar = cotizacion
    dolar_formateado = dolar[0:6]
    # print(dolar[0:6] + " ")
    print(dolar_formateado)

print(" - Hora act. " + tabla_hora.text[20:25])

path_actual = os.getcwd()
# print(path_actual)
# Abro el archivo valorDolar.txt donde almaceno el valor dolar.
valorArchivo = open(path_actual+'/cotizacion.txt', "r+")
#valorArchivo = open('/home/fideo/proyectos/cotizacionDolar/cotizacion.txt', "r+")
cotizacionActual = valorArchivo.read(17).strip("\n")

print(cotizacionActual[0:6] + " - " + dolar[0:6])
print(cotizacionActual[12:17] + " - " + tabla_hora.text[20:25])
hora_actual = tabla_hora.text[20:25]

app_icon_path = os.path.join(path_actual, "iconoDolar.ico")

if (cotizacionActual[0:6] != dolar[0:6]) or (cotizacionActual[12:17] != tabla_hora.text[20:25]):
    
    # Configuración de rutas según entorno (ejecutable o script .py)
    BASE_DIR = (
        os.path.dirname(sys.executable)
        if getattr(sys, "frozen", False)
        else os.path.dirname(os.path.abspath(__file__))
    )

    path_valor = os.path.join(BASE_DIR, "valorDolar.txt")
    path_hora = os.path.join(BASE_DIR, "horaDolar.txt")
    path_icono = os.path.join(BASE_DIR, "iconoDolar.ico")

    # --- Lectura de Estados Anteriores ---
    valor_anterior = ""
    if os.path.exists(path_valor):
        with open(path_valor, "r", encoding="utf-8") as f:
            valor_anterior = f.read().strip()

    hora_anterior = ""
    if os.path.exists(path_hora):
        with open(path_hora, "r", encoding="utf-8") as f:
            hora_anterior = f.read().strip()

    # --- Verificación de Cambios ---
    hubo_cambio_valor = valor_anterior != dolar_formateado
    hubo_cambio_hora = hora_anterior != hora_actual

    # --- Verificación de Cambios ---
    hubo_cambio_valor = valor_anterior != dolar_formateado
    hubo_cambio_hora = hora_anterior != hora_actual


    if hubo_cambio_valor:
        titulo = "CAMBIÓ LA COTIZACIÓN DEL DÓLAR"
        mensaje = f"Nuevo valor: ${dolar_formateado} (Hora: {hora_actual})"
    else:
        titulo = "ACTUALIZACIÓN DE HORARIO DÓLAR"
        mensaje = f"Valor actual: ${dolar_formateado} (Nueva Hora: {hora_actual})"

    # Disparar notificación nativa de Windows
    toaster = InteractableWindowsToaster("Cotizador Dólar BNA")
    
    toast = Toast()
    toast.text_fields = [titulo, mensaje]

    # Si existe el ícono, se agrega convirtiendo la ruta con ToastDisplayImage
    if os.path.exists(path_icono):
        from windows_toasts import ToastDisplayImage
        toast.AddImage(ToastDisplayImage.fromPath(path_icono))
        
    toaster.show_toast(toast)
    time.sleep(1)

    '''notification.notify(
        title="CAMBIÓ LA COTIZACIÓN DEL DOLAR",
        message=dolar_formateado,
        # app_icon="/home/fideo/proyectos/cotizacionDolar/iconoDolar.ico",
        app_icon= app_icon_path,
        # displaying time
        timeout=10
        )
    time.sleep(5)
    '''

# Me posiciono en el primer lugar del documento para actualizar el archivo.
valorArchivo.seek(0, 0)
# escribo el valor del dólar y le digo que tome desde la posición 0 hasta la 6 dolar[0:6]
valorArchivo.write(dolar[0:6])
valorArchivo.write(" Hora ")
valorArchivo.write(tabla_hora.text[20:25])


valorArchivo.close()
