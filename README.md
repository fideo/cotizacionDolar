# Cotización Dolar según BNA

Obtengo la cotización de la moneda Peso Argentino según el Banco Nación de Argentina.

Este programa en Python obtiene la cotización del dolar haciendo un webscraping desde el sitio de BNA

Para ejecutar este programa se necesita tener instalado Python 3.11 o superior:

Crear un entorno virtual con el siguiente comando:
python -m venv venv

Luego ingresamos al entorno virtual con el comando:
source venv/bin/activate #linux
source vnv/Scripts/activate #windows

Una vez dentro del entorno virtual, se instalan las dependencias con el siguiente comando:
pip install -r requirements.txt

Para generar el .exe se ejecuta esta sentencia:
pyinstaller --onefile --collect-all plyer cotizacionDolar.py

La linea siguiente es para que no muestre la ventanda de consola:
pyinstaller --onefile --noconsole --collect-all plyer cotizacionDolar.py 

Para que muestre el popup en sistemas GNU/Linux debemos realizar lo siguiente:
Crear el servicio
~/.config/systemd/user/cotizacion.service
```
[Unit]
Description=Cotización dólar

[Service]
Type=oneshot
WorkingDirectory=/home/fideo/proyectos/cotizacionDolar
ExecStart=/home/fideo/proyectos/cotizacionDolar/venv/bin/python cotizacionDolar.py
```

Luego configuración del timer
```
~/.config/systemd/user/cotizacion.timer
[Unit]
Description=Cotización dólar cada 5 minutos

[Timer]
OnBootSec=1min
OnUnitActiveSec=5min

[Install]
WantedBy=timers.target
```