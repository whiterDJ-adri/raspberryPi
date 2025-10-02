# Reto II - RaspberryPi

## Raspberry OS

- https://downloads.raspberrypi.com/raspios_arm64/images/raspios_arm64-2025-05-13/
- https://www.raspberrypi.com/software/

Como proyecto de Raspberry Pi nos hemos propuesto que una webcam registre, con imágenes, si hay movimiento. Dichas imágenes se guardan
en una carpeta que, a su vez, se guarda en una DDBB.
Se registra:
 - Tiempo
 - Hora
 - Persona cargo en su momento

Tendrá una interfaz web hecha con HTML, CSS y JS


Como opcional/extra
- Una vez hecha la base, con ayuda de n8n, lo enviamos a un canal de mensajeria (Discord)

##Aspectos a cubrir
 - Configuración de una base de datos no relacional como MongoDB
 - Creación de una API para la conexión con Raspberry
 - ApI para el frontend y ciertas partes de la Raspberry
 - Aplicaremos una estructura MVC para este proyecto

##Elementos que se utiliza de la Raspberry
- Hacer el modulo que interactua con los sensores (web y sensores)
- Despliege de código fuente en la raspberry
- Conexión de la base de datos de la Raspberry con post a un canal con n8n. La raspberry siempre estará encendida
