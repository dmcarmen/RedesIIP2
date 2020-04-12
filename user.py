import requests
from Crypto.PublicKey import RSA

#TODO token global pls
headers = {'Authorization': "Bearer " + token}
url = 'https://vega.ii.uam.es:8080/api/users/'

def create_id(nombre, email, alias):
    
    # Creamos el par de claves
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    print("Generando par de claves RSA de 2048 bits...OK")

    url += 'register'
    args = {'nombre': nombre, 'email': email, 'alias': alias, 'publicKey': publicKey}
    
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
    url += 'search'
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
            i += 1
            print("[{}] {}, {}, ID: {}".format(i, nombre, email, userID))

def delete_id(userID):
    url += 'delete'
    args = {'userID': userID}

    try:
        r = requests.post(url, headers = headers, json = args)
    except requests.ConnectionError:
        print("Error de conexion")
        return
    
    print("Solicitando borrado de la identidad #{}...OK".format(userID))
    if r.status_code == requests.codes.ok:
        #TODO curl bc pisto
        answer = r.json()
        userID = answer.get('userID') #TODO poco logico maybe meeh
        print("Identidad con ID#{} borrada correctamente".format(userID))

