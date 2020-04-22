import os

# Variable global del token
token = ""


def config_ini():
    """
        Nombre: config_ini
        Descripcion: Realiza la configuración inicial necesaria.
            Lee de token.txt el token del usuario.
        Argumentos: Ninguno
        Retorno: Ninguno
    """
    global token

    # Leemos token.txt y lo guardamos en la variable global token
    if os.stat("token.txt").st_size == 0:
        print("Error: no hay token")
    else:
        file = open("token.txt", "r")
        token = file.read()[:-1]


# Guardamos el token
config_ini()

def error(request):
    """
        Nombre: error
        Descripcion: Imprime el mensaje de error correspodiente recibido por una
            request.
        Argumentos:
            - request: respuesta de la peticion al servidor.
        Retorno: Ninguno
    """
    json = request.json()

    # Si el error esta definido imprimimos la informacion completa
    if "error_code" in json:
        print("Error {}: {} -> {}".format(json.get("http_error_code"), json.get("error_code"), json.get("description")))
    else:
        print("Error {}".format(request.status_code))
