import time
import requests
from bs4 import BeautifulSoup
from plyer import notification

# Obtengo la url del sitio a obtener los datos
url = 'https://www.bna.com.ar/Personas'

# A traves de request obtengo todo el codigo de la url pasada
r = requests.get(url)

# Paso a BeautifulSoup lo obtenido como texto y lo parseo como HTML
soup = BeautifulSoup(r.text, 'html.parser')

# Busco el tag table con class table cotizacion
tabla_dolar = soup.find('table', class_='table cotizacion')
tabla_hora = soup.find('div', class_='legal')

dolar = 0

# Recorro la tabla encontrando los tags tbody
for cotizacion in tabla_dolar.find_all('tbody'):
  dolar = cotizacion.find_all('td')[2].text
  dolar_formateado = dolar[0:6] + " "
  #print(dolar[0:6] + " ")
  print(dolar_formateado)

print("Hora act. " + tabla_hora.text[20:25])

# Abro el archivo valorDolar.txt donde almaceno el valor dolar.
valorArchivo = open('/home/fideo/proyectos/cotizacionDolar/cotizacion.txt', "r+")
cotizacionActual=valorArchivo.read(10).strip("\n")

#if cotizacionActual != dolar:
#    notification.notify(
#                title="CAMBIÓ LA COTIZACIÓN DEL DOLAR",
#                message=dolar_formateado,
#
#                # displaying time
#                timeout=2
#        )
#    time.sleep(10)

# Me posiciono en el primer lugar del documento para actualizar el archivo.
valorArchivo.seek(0, 0)
# escribo el valor del dolar y le digo que tome desde la posición 0 hasta la 6 dolar[0:6]
valorArchivo.write(dolar[0:6])
valorArchivo.write(" Hora ")
valorArchivo.write(tabla_hora.text[20:25])


valorArchivo.close()
