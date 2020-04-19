import requests
import utils as u

u.config_ini()
headers = {'Authorization': "Bearer " + u.token}
urlIni = 'https://tfg.eps.uam.es:8080/api/files/'
path_archivos = "Archivos/"

def upload(dest_id, file_path):
    f = open(file_path, "rb")
    mensaje = f.read()
    f.close()
    file_name = os.path.basename(file_path)
    path_archivo = path_archivos+file_name

    print("Solicitando envio de fichero a SecureBox")
    mensaje_sign = sign(mensaje)
    if sign is None:
        return

    print("Recuperando clave pública de ID {}...".format(dest_id), end="")
    clave_pub_r = get_public_key(dest_id)
    print("OK")

    mensaje_enc_sign = encrypt(mensaje, clave_pub_r)

    # Guardamos el fichero encriptado y firmado
    f = open(path_archivo,"wb")
    f.write(mensaje_enc_sign)
    f.close()

    #TODO ufile=@/home/  / .py con path_archivo
    print("Subiendo fichero a servidor...", end="")
    url = urlIni + "upload"
    try:
        r = requests.post(url, headers=headers)
    except requests.ConnectionError:
        print("\nError de conexion")
        return

    if r.status_code == requests.codes.ok:
        print("OK")
        answers = r.json()
        files_id = answers.get('files_id')
        file_size = answers.get('file_size') #TODO que hacer con file_size?
        print("Subida realizada correctamente, ID del fichero: {}".format(files_id))
    else:
        u.error(r)


def download(file_id, source_id):
    print("Descargando fichero de SecureBox...", end="")
    url = urlIni + "download"
    args = {'file_id': file_id}
    try:
        r = requests.post(url, headers=headers, json=args)
    except requests.ConnectionError:
        print("Error de conexion")
        return

    if r.status_code == requests.codes.ok:
        print("OK")
        print("-> {} bytes descargados correctamente".format(len(r)))

        print("-> Descifrando fichero...", end="")
        mensaje_descifrado = decrypt(r)
        if mensaje_descifrado is None:
            return
        print("OK")

        print("-> Recuperando clave pública de ID {}...".format(source_id))
        clave_pub_e = get_public_key(source_id)
        print("OK")

        print("-> Verificando firma...", end="")
        mensaje_original = check_sign(mensaje_descifrado, clave_pub_e)
        if mensaje_original is None:
            return
        print("OK")

        #TODO guardar el fichero

        print("Fichero descargado y verificado correctamente")
    else:
        u.error(r)

def delete(file_id):
    url = urlIni + "delete"
    args = {'file_id': file_id}
    print("Solicitando borrado del fichero #{}...".format(file_id),end="")
    try:
        r = requests.post(url, headers=headers, json=args)
    except requests.ConnectionError:
        print("\nError de conexion")
        return

    if r.status_code == requests.codes.ok:
        print("OK")
        answer = r.json()
        file_id = answer.get('file_id')
        print("Fichero con ID#{} borrado correctamente".format(file_id))
    else:
        u.error(r)

def list_files(userID):
    url = urlIni + "list"
    args = {'userID': userID}
    print("Buscando ficheros del usuario #{} en el servidor".format(userID),end="")
    try:
        r = requests.post(url, headers=headers, json=args)
    except requests.ConnectionError:
        print("\nError de conexion")
        return

    if r.status_code == requests.codes.ok:
        print("OK")
        answers = r.json()
        files_list = answers.get('files_list')
        num_files = answers.get('num_files')
        print("{} ficheros encontrados:".format(num_files))
        i=0
        for file in files_list:
            print("[{}] #{}".format(i,file))
            i+=1
    else:
        u.error(r)
