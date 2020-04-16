import requests
from Crypto.PublicKey import RSA
import utils as u

u.config_ini()
headers = {'Authorization': "Bearer " + u.token}
urlIni = 'https://tfg.eps.uam.es:8080/api/users/'

def create_id(nombre, email):
    global urlIni, headers
    # Creamos el par de claves
    print("Generando par de claves RSA de 2048 bits")
    key = RSA.generate(2048)
    privateKey = key.export_key()
    publicKey = key.publickey().export_key()
    url = urlIni + 'register'
    args = {'nombre': nombre, 'email': email, 'publicKey': publicKey}
    
    try:
        r = requests.post(url, headers = headers, json = args)
    
    except requests.ConnectionError:
        print("Error de conexion")
        return
    
    if r.status_code == requests.codes.ok:
        # Guardamos la clave privada ya que el usuario se crea correctamente
        #TODO ver como guardar 
        #file_out = open("private.pem", "wb")
        #file_out.write(private_key)
        answer = r.json()
        userID = answer.get('userID')
        print("Identidad con ID# {} creada correctamente".format(userID))
    else:
        u.error(r)
    

def search_id(data_search):
    global urlIni, headers
    url = urlIni + 'search'
    args = {'data_search': data_search}
    print("Buscando usuario '" + data_search + "' en el servidor")
    try:
        r = requests.post(url, headers = headers, json = args)
    except requests.ConnectionError:
        print("Error de conexion")
        return
    
    if r.status_code == requests.codes.ok:
        answers = r.json()
        print("{} usuarios encontrados:".format(len(answers)))
        i = 0
        for answer in answers:
            print("[{}] {}, {}, ID: {}".format(i+1, answers[i]['nombre'], answers[i]['email'], answers[i]['userID']))
            i += 1
    else:
        u.error(r)

def delete_id(userID):
    global urlIni, headers
    url = urlIni + 'delete'
    args = {'userID': userID}
    print("Solicitando borrado de la identidad #{}".format(userID))

    try:
        r = requests.post(url, headers = headers, json = args)
    except requests.ConnectionError:
        print("Error de conexion")
        return
    
    if r.status_code == requests.codes.ok:
        answer = r.json()
        userID = answer.get('userID') #TODO poco logico maybe porque argumento pero meeh
        print("Identidad con ID#{} borrada correctamente".format(userID))
    else:
        u.error(r)

def prueba():
    create_id("Carmen", "carmen.diezmenendez@estudiante.uam.es")
    search_id("Carmen")
    #delete_id(383336)
    #search_id("Carmen")
    delete_id(38333336)

prueba()
