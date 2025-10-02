# Utilizar un servicio externo para la gestión de variables de entorno

## Motivación

Utilizar un servicio externo para la gestión de variables de entorno nos permite evitar la exposición de variables de entorno en el código fuente. En este caso, utilizaremos la plataforma [Infisical](https://infisical.com/). Infical es de codigo abierto y gratuito, nos permite configurar variables de entorno de manera colaborativa y mantenerlas sincronizadas en todos los entornos.

## Configuración

1. Crear una cuenta en [Infisical](https://infisical.com/)
2. Tener acceso al proyecto compartido de claves
3. Una vez hecho esto, decargamos el CLI de infisical

```bash
winget install infisical
```

4. Abrimos una nueva pestaña en la terminal para obtener los cambios y accedemos a la carpeta /backend

```bash
infisical login
infisical init
```

5. Una vez incializado el proyecto, podemos ejecutar el proyecto psandole las variables de la siguiente manera

```bash
infisical run --env=dev python main.py
```
