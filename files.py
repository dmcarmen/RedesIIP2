import requests
import utils as u

u.config_ini()
headers = {'Authorization': "Bearer " + u.token}
urlIni = 'https://tfg.eps.uam.es:8080/api/files/'

#TODO como guardamos contraseñas
#TODO crear otro fichero al encriptar
def upload(dest_id, fichero):
    print("Solicitando envio de fichero a SecureBox")
    #TODO ver si enc_sign(mensaje, clave_priv_e, clave_pub_r) o de otra forma
    fichero_enc_sign = enc_sign(fichero, clave_pub_r)
    if fichero_enc_sign is None:
        return

    #TODO ufile=@/home/  / .py
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

        #TODO separar esta funcion en dos para decrypt, obtener clave y check_sign
        #check_sign_and_decrypt(mensaje, clave_pub_e, clave_priv_r)
        if check_sign_and_decrypt(mensaje, clave_pub_e) is None:
            return

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
