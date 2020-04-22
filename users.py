import requests
from Crypto.PublicKey import RSA
import utils as u

u.config_ini()
headers = {'Authorization': "Bearer " + u.token}
urlIni = 'https://tfg.eps.uam.es:8080/api/users/'


def create_id(nombre, email):
    """
        Nombre: create_id
        Descripcion: Funcion que manda una peticion a la API para crear un usuario. Crea el par de claves RSA,
            guarda la privada y envía la publica a la API.
            En caso de error lo imprime por pantalla y sale de la funcion.
        Argumentos:
            -nombre: nombre del usuario a crear.
            -email: email del usuario.
        Retorno: Ninguno
    """
    global urlIni, headers
    # Creamos el par de claves
    print("Generando par de claves RSA de 2048 bits...", end="")
    key = RSA.generate(2048)
    public_key = key.publickey().export_key()
    print("OK")

    # Enviamos la peticion a la API
    url = urlIni + 'register'
    args = {'nombre': nombre, 'email': email, 'publicKey': public_key}
    try:
        r = requests.post(url, headers=headers, json=args)
    except requests.ConnectionError:
        print("Error de conexion")
        return

    # Si la peticion es correcta guardamos la clave privada del usuario e imprimimos su ID
    if r.status_code == requests.codes.ok:
        f = open("clave.pem", "wb")
        f.write(key.export_key('PEM'))
        f.close()
        answer = r.json()
        user_id = answer.get('userID')
        print("Identidad con ID#{} creada correctamente".format(user_id))
    else:
        print()
        u.error(r)


def search_id(data_search):
    """
        Nombre: search_id
        Descripcion: Busca un usuario cuyo nombre o correo electronico contenga cadena en el repositorio
            de identidades de SecureBox, e imprime su ID.
            En caso de error lo imprime por pantalla y sale de la funcion.
        Argumentos:
            -data_search: cadena a buscar.
        Retorno: Ninguno
    """
    global urlIni, headers

    # Enviamos la peticion a la API
    url = urlIni + 'search'
    args = {'data_search': data_search}
    print("Buscando usuario '" + data_search + "' en el servidor...", end="")
    try:
        r = requests.post(url, headers=headers, json=args)
    except requests.ConnectionError:
        print("\nError de conexion")
        return
    # Si es correcta imprimimos todas las coincidencias devueltas
    if r.status_code == requests.codes.ok:
        print("OK")
        answers = r.json()
        print("{} usuarios encontrados:".format(len(answers)))
        i = 0
        for answer in answers:
            print("[{}] {}, {}, ID: {}".format(i + 1, answer['nombre'], answer['email'], answer['userID']))
            i += 1
    else:
        print()
        u.error(r)


def delete_id(user_id):
    """
        Nombre: delete_id
        Descripcion: Borra la identidad con ID id registrada en el sistema. Solo puede borrar la suya propia.
            En caso de error lo imprime por pantalla y sale de la funcion.
        Argumentos:
            -userID: ID a borrar.
        Retorno: Ninguno
    """
    global urlIni, headers

    # Envia la peticion a la API
    url = urlIni + 'delete'
    args = {'userID': user_id}
    print("Solicitando borrado de la identidad #{}...".format(user_id), end="")
    try:
        r = requests.post(url, headers=headers, json=args)
    except requests.ConnectionError:
        print("\nError de conexion")
        return

    # Si la peticion es correcta imprimimos el ID eliminado
    if r.status_code == requests.codes.ok:
        print("OK")
        answer = r.json()
        user_id = answer.get('userID')
        print("Identidad con ID#{} borrada correctamente".format(user_id))
    else:
        print()
        u.error(r)


def get_public_key(user_id):
    """
        Nombre: get_public_key
        Descripcion: Obtiene la clave pública de un usuario.
            En caso de error lo imprime por pantalla y sale de la funcion.
        Argumentos:
            -userID: ID a borrar.
        Retorno: la clave publica o None en caso de error.
    """
    global urlIni, headers

    # Enviamos la peticion a la API
    url = urlIni + 'getPublicKey'
    args = {'userID': user_id}
    print("Solicitando clave de la identidad #{}".format(user_id), end="")
    try:
        r = requests.post(url, headers=headers, json=args)
    except requests.ConnectionError:
        print("\nError de conexion")
        return None

    if r.status_code == requests.codes.ok:
        print("OK")
        return RSA.import_key(r.json().get('publicKey'))
    else:
        print()
        u.error(r)
        return None


def prueba():
    create_id("Carmen", "carmen.diezmenendez@estudiante.uam.es")
    search_id("Carmen")
    delete_id(38333336)
