import requests

urlIni = 'https://tfg.eps.uam.es:8080/api/files/'

#TODO como guardamos contraseñas
#TODO se crea otro fichero al encriptar?
def upload(dest_id, fichero):
    #TODO ver si enc_sign(mensaje, clave_priv_e, clave_pub_r) o de otra forma
    fichero_enc_sign = enc_sign(fichero, clave_pub_r)
    if fichero_enc_sign is None:
        return

    #TODO ufile=
    print("Subiendo fichero a servidor...", end="")
    url = urlIni + "upload"
    r = requests.post(url) #TODO si va mal la request
    print("OK")

def download(file_id, source_id):
    print("Descargando fichero de SecureBox...", end="")
    url = urlIni + "download"
    args = {'file_id': file_id}
    r = requests.post(url, json=args)
    print("OK")

    #TODO check si en r contenido binario bien es decir mensaje
    if r.status_code == requests.codes.ok:
        mensaje= r
        print("-> {} bytes descargados correctamente".format(len(mensaje)))

        #check_sign_and_decrypt(mensaje, clave_pub_e, clave_priv_r)
        if check_sign_and_decrypt(mensaje, clave_pub_e) is None:
            return
        #TODO nombre del fichero
        print("Fichero '{}' descargado y verificado correctamente".format())

def delete(file_id):
    url = urlIni + "delete"
    args = {'file_id': file_id}
    r = requests.post(url, json=args)

def list_files(userID):
    url = urlIni + "list"
    args = {'userID': userID}
    r = requests.post(url, json=args)
    if r.status_code == requests.codes.ok:
