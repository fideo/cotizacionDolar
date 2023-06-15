import time
import requests
import os
from bs4 import BeautifulSoup
from plyer import notification

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
for cotizacion in tabla_dolar.find_all('tbody'):
    dolar = cotizacion.find_all('td')[2].text
    dolar_formateado = dolar[0:6]
    # print(dolar[0:6] + " ")
    print(dolar_formateado)

print(" - Hora act. " + tabla_hora.text[20:25])

path_actual = os.getcwd()
# print(path_actual)
# Abro el archivo valorDolar.txt donde almaceno el valor dolar.
# valorArchivo = open(path_actual+'/cotizacion.txt', "r+")
valorArchivo = open('/home/fideo/proyectos/cotizacionDolar/cotizacion.txt', "r+")
cotizacionActual = valorArchivo.read(17).strip("\n")

# print(cotizacionActual[0:6] + " - " + dolar[0:6])
# print(cotizacionActual[12:17] + " - " + tabla_hora.text[20:25])

if (cotizacionActual[0:6] != dolar[0:6]) or (cotizacionActual[12:17] != tabla_hora.text[20:25]):
    notification.notify(
        title="CAMBIÓ LA COTIZACIÓN DEL DOLAR",
        message=dolar_formateado,
        app_icon="/home/fideo/proyectos/cotizacionDolar/iconoDolar.ico",
        # displaying time
        timeout=10
        )
    time.sleep(5)

# Me posiciono en el primer lugar del documento para actualizar el archivo.
valorArchivo.seek(0, 0)
# escribo el valor del dólar y le digo que tome desde la posición 0 hasta la 6 dolar[0:6]
valorArchivo.write(dolar[0:6])
valorArchivo.write(" Hora ")
valorArchivo.write(tabla_hora.text[20:25])


valorArchivo.close()
