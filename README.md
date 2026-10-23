# Cotización Dolar según BNA

Obtengo la cotización de la moneda Peso Argentino según el Banco Nación de Argentina.

Este programa en Python obtiene la cotización del dolar haciendo un webscraping desde el sitio de BNA

Para generar el .exe se ejecuta esta sentencia:
pyinstaller --onefile --collect-all plyer cotizacionDolar.py

La linea siguiente es para que no muestre la ventanda de consola:
pyinstaller --onefile --noconsole --collect-all plyer cotizacionDolar.py 