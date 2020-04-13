import requests
from Crypto.PublicKey import RSA

token = ""
#TODO token global pls
headers = {'Authorization': "Bearer " + token}
urlIni = 'https://tfg.eps.uam.es:8080/api/users/'

def create_id(nombre, email):
    global urlIni, headers
    # Creamos el par de claves
    key = RSA.generate(2048)
    privateKey = key.export_key()
    publicKey = key.publickey().export_key()
    print("Generando par de claves RSA de 2048 bits...OK")
    url = urlIni + 'register'
    args = {'nombre': nombre, 'email': email, 'publicKey': publicKey}
    
    try:
        r = requests.post(url, headers = headers, json = args)
    except requests.ConnectionError:
        print("Error de conexion")
        return
    
    if r.status_code == requests.codes.ok:
        #TODO ver como guardar y probar con curl que devuelve...
        #file_out.write(private_key)
        #file_out = open("private.pem", "wb")
        answer = r.json()
        userID = answer.get('userID')
        #ts = answer.get('ts')
        print("Identidad con ID# {} creada correctamente".format(userID))

def search_id(data_search):
    global urlIni, headers
    url = urlIni + 'search'
    args = {'data_search': data_search}
    try:
        r = requests.post(url, headers = headers, json = args)
    except requests.ConnectionError:
        print("Error de conexion")
        return
    
    if r.status_code == requests.codes.ok:
        print("Buscando usuario '" + data_search + "' en el servidor...OK")
        #TODO curl bc pisto
        answers = r.json()
        print("{} usuarios encontrados:".format(len(answers)))
        i = 0
        for answer in answers:
            print("[{}] {}, {}, ID: {}".format(i+1, answers[i]['nombre'], answers[i]['email'], answers[i]['userID']))
            i += 1

def delete_id(userID):
    global urlIni, headers
    url = urlIni + 'delete'
    args = {'userID': userID}

    try:
        r = requests.post(url, headers = headers, json = args)
    except requests.ConnectionError:
        print("Error de conexion")
        return
    
    if r.status_code == requests.codes.ok:
        print("Solicitando borrado de la identidad #{}...OK".format(userID))
        #TODO curl bc pisto
        answer = r.json()
        userID = answer.get('userID') #TODO poco logico maybe meeh
        print("Identidad con ID#{} borrada correctamente".format(userID))

def prueba():
    create_id("Carmen", "carmen.diezmenendez@estudiante.uam.es")
    search_id("Carmen")
    delete_id(383336)
    search_id("Carmen")

prueba()
