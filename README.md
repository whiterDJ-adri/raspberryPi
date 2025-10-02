
# Raspberry OS

- <https://downloads.raspberrypi.com/raspios_arm64/images/raspios_arm64-2025-05-13/>  
- <https://www.raspberrypi.com/software/>  

Como proyecto con Raspberry Pi, nos hemos propuesto que una webcam registre, mediante imágenes, si hay movimiento. Dichas imágenes se guardarán en una carpeta que, a su vez, se almacenará en una base de datos (BBDD).  

Se registrará:  

- Fecha  
- Hora  
- Persona responsable en ese momento  

El proyecto contará con una interfaz web hecha con **HTML, CSS y JavaScript**.  

## Opcional / Extra

- Una vez desarrollada la base, con ayuda de **n8n**, enviaremos las capturas a un canal de mensajería (por ejemplo, Discord).  

## Aspectos a cubrir

- Configuración de una base de datos no relacional como **MongoDB**  
- Creación de una **API** para la conexión con la Raspberry Pi  
- API para el frontend y ciertas partes de la Raspberry Pi  
- Aplicación de una estructura **MVC** para este proyecto  

## Elementos a utilizar de la Raspberry Pi

- Desarrollo del módulo que interactúe con los sensores (web y sensores físicos)  
- Despliegue del código fuente en la Raspberry Pi  
- Conexión de la base de datos de la Raspberry Pi con un flujo de publicación (POST) hacia un canal mediante **n8n**. La Raspberry permanecerá siempre encendida.
