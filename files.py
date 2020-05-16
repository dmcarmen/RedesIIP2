import requests
import utils as u
import os
import users
import crypto

urlIni = 'https://tfg.eps.uam.es:8080/api/files/'


def upload(file_path, dest_id):
    """
        Nombre: upload
        Descripcion: Envia un fichero a otro usuario.
            Subimos el archivo a SecureBox firmado y cifrado con las claves adecuadas
            para que pueda ser recuperado y verificado por el destinatario.
            En caso de error lo imprime por pantalla y sale de la funcion.
        Argumentos:
            -dest_id: ID del user que recibira el archivo.
            -file_path: path del archivo a subir.
        Retorno: Ninguno
    """

    print("Solicitando envio de fichero a SecureBox")

    # Abrimos el archivo y vemos donde guardar el cifrado y firmado temporalmente
    try:
        f = open(file_path, "rb")
    except FileNotFoundError:
        print("El archivo no existe")
        return

    mensaje = f.read()
    f.close()
    file_name = os.path.basename(file_path)
    path_archivo = os.path.abspath(u.path_archivos + file_name)

    # Conseguimos la clave publica de dest_id
    clave_pub_r = users.get_public_key(dest_id)
    if clave_pub_r is None:
        print("Error al obtener la clave publica")
        return

    # Firmamos y ciframos el fichero
    mensaje_enc_sign = crypto.enc_sign(mensaje, clave_pub_r)
    if mensaje_enc_sign is None:
        return

    # Guardamos el fichero encriptado y firmado
    f = open(path_archivo, "wb")
    f.write(mensaje_enc_sign)
    f.close()

    # Enviamos la peticion a la API
    print("-> Subiendo fichero a servidor...", end="")
    url = urlIni + "upload"
    files = {'ufile': open(path_archivo, "rb")}
    try:
        r = requests.post(url, headers=u.headers, files=files)
    except requests.ConnectionError:
        print("\nError de conexion")
        return

    # Si es correcto imprimimos el ID del archivo
    if r.status_code == requests.codes.ok:
        print("OK")
        answers = r.json()
        file_id = answers.get('file_id')
        print("Subida realizada correctamente, ID del fichero: {}".format(file_id))
        # Borramos el archivo auxiliar
        os.remove(path_archivo)
    else:
        print()
        u.error(r)


def download(file_id, source_id):
    """
        Nombre: download
        Descripcion: Recupera un fichero con ID id_fichero del sistema.
            Tras ser descargado, desciframos el contenido y verificamos la firma.
            En caso de error lo imprime por pantalla y sale de la funcion.
        Argumentos:
            -file_id: ID del fichero en el sistema.
            -source_id: ID del user al que pertenece.
        Retorno: Ninguno
    """
    print("Descargando fichero de SecureBox...", end="")

    # Enviamos la peticion a la API
    url = urlIni + "download"
    args = {'file_id': file_id}
    try:
        r = requests.post(url, headers=u.headers, json=args)
    except requests.ConnectionError:
        print("Error de conexion")
        return

    # Si es correcto recuperamos el mensaje
    if r.status_code == requests.codes.ok:
        print("OK")
        print("-> {} bytes descargados correctamente".format(r.headers.get('Content-Length')))

        mensaje_descifrado = crypto.decrypt(r.content)
        if mensaje_descifrado is None:
            return

        # Recuperamos la clave publica del usuario y verificamos la firma
        clave_pub_e = users.get_public_key(source_id)
        if clave_pub_e is None:
            print("Error al obtener la clave publica")
            return

        mensaje_original = crypto.check_sign(mensaje_descifrado, clave_pub_e)
        if mensaje_original is None:
            return

        # Hallamos el nombre del fichero
        aux = r.headers.get('content-disposition')
        nombre = (aux.split("=")[1]).replace('"', '')

        # Guardamos el fichero en path_archivos
        f = open(u.path_archivos + nombre, 'wb')
        f.write(mensaje_original)
        f.close()

        print("Fichero descargado y verificado correctamente")
    else:
        print()
        u.error(r)


def delete(file_id):
    """
        Nombre: delete
        Descripcion: Borra un fichero del sistema.
            En caso de error lo imprime por pantalla y sale de la funcion.
        Argumentos:
            -file_id: ID del fichero en el sistema.
        Retorno: Ninguno
    """
    # Enviamos la peticion a la API
    url = urlIni + "delete"
    args = {'file_id': file_id}
    print("Solicitando borrado del fichero #{}...".format(file_id), end="")
    try:
        r = requests.post(url, headers=u.headers, json=args)
    except requests.ConnectionError:
        print("\nError de conexion")
        return

    if r.status_code == requests.codes.ok:
        print("OK")
        answer = r.json()
        file_id = answer.get('file_id')
        print("Fichero con ID#{} borrado correctamente".format(file_id))
    else:
        print()
        u.error(r)


def list_files():
    """
        Nombre: list_files
        Descripcion: Lista todos los ficheros pertenecientes al usuario.
            En caso de error lo imprime por pantalla y sale de la funcion.
        Argumentos: Ninguno
        Retorno: Ninguno
    """
    # Enviamos la peticion a la API
    url = urlIni + "list"
    print("Buscando ficheros del usuario en el servidor...", end="")
    try:
        r = requests.post(url, headers=u.headers)
    except requests.ConnectionError:
        print("\nError de conexion")
        return

    # Si es correcta impimimos todos los ficheros del usuario
    if r.status_code == requests.codes.ok:
        print("OK")
        answers = r.json()
        files_list = answers.get('files_list')
        num_files = answers.get('num_files')
        print("{} ficheros encontrados:".format(num_files))
        i = 0
        for file in files_list:
            i += 1
            print("[{}] ID#{} {}".format(i, file.get('fileID'), file.get('fileName')))
    else:
        print()
        u.error(r)


def prueba_files():
    # upload('383336', 'Prueba.txt')
    # delete('De29fbC4')
    list_files('383336')
    download('6edD0F29', '383336')
