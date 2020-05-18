## Mejoras
- Ampliadas decisiones de diseño y seguridad sobre el fichero de configuración (apartado de **Configuración inicial y seguridad del token**).
- Arreglado `list_files` (no pide `source_id`).
- Error con `create_id` y los bytes arreglado instalando [simplejson](https://simplejson.readthedocs.io/en/latest/).

## Extras
- Protegemos el fichero de configuración, y con él el token, encriptándolo con una contraseña. Guardamos su hash para comprobarla cada vez que el usuario use la aplicación.
- Añadimos los endpoints de la API al fichero de configuración.
