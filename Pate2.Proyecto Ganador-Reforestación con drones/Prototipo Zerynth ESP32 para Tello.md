# Prototipo dron sembrador de árboles
![](img/Sistema%20dron%20sembrador.png)

La imagen describe el modelo protipo propuesto por Geotemelos para un dron
que no posee un GPS pero carga con el dispensador de semillas. Los comandos se envían
desde un celular o laptop que reciben los reportes de ubicación relativa con este, el mismo
que localiza a través de GPS para una siembra de precisión.

Sin embargo, para el proptotipo avanzado hasta la presentación en la compentencia, la
siguiente imagen es lo implementado.
![](img/proptipo_baja_resol.png)

## ESP32 + Zerynth
La versatilidad y multi dispositivo que ofrece Zerynth SDK es aprovechado aquí pues
el código Python es de alto nivel, permitiendo enfocarse en el objetivo principal
del proyecto y desatender detalles necesarios para usar un micro controlador.
Una introducción amigable al uso de este SDK está en esta URL:
[Python on ESP32 – Getting Started](https://www.zerynth.com/blog/python-on-esp32-getting-started/).

### Código dispensador prototipo
El código base ejecuta el dispensador cada vez que el dron se mueve a una esquina de un cuadrado de 1 metro por lado. Esto, por supuesto, será escalado correctamente debido a las funciones escritas.
Si desea leer el código, este estará en la carpeta **zerynth_esp32_scripts**.
Aquí tiene unos enlaces para abrir directamente los scripts:
- [main.py](./zerynth_esp32_scripts/main.py)
- [dispense.py](./zerynth_esp32_scripts/dispense.py)

