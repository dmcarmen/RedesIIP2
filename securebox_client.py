import argparse
import users
#import files
import crypto

#TODO control de errores, specially los de coger datos como get publicKey

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interactúa con securebox')

    parser.add_argument('--create_id', help='Crea una nueva identidad (par de claves púlica y privada) para un usuario con nombre nombre y correo email, y la registra en SecureBox, para que pueda ser encontrada por otros usuarios', nargs=2, metavar = ('Nombre', 'Email'))

    parser.add_argument('--search_id', help='Busca un usuario cuyo nombre o correo electrónico contenga cadena en el repositorio de identidades de SecureBox, y devuelve su ID', metavar = 'Nombre/Email')

    parser.add_argument('--delete_id', help='Borra la identidad con ID id registrada en el sistema', metavar = 'id')

    parser.add_argument('--upload', help='Envia un fichero a otro usuario, cuyo ID es especificado con la opción --dest_id', metavar = 'fichero')

    parser.add_argument('--source_id', help='ID del emisor del fichero', metavar = 'id_emisor')

    parser.add_argument('--dest_id', help='ID del receptor del fichero', metavar = 'id_receptor')

    parser.add_argument('--list_files', action='store_true', help='Lista todos los ficheros pertenecientes al usuario')

    parser.add_argument('--download', help='Recupera un fichero con ID id_fichero del sistema', metavar = 'id_fichero')

    parser.add_argument('--delete_file', help='Borra un fichero del sistema', metavar = 'id_fichero')

    parser.add_argument('--encrypt', help='Cifra un fichero, de forma que puede ser descifrado por otro usuario, cuyo ID es especificado con la opción --dest_id', metavar = 'fichero')

    parser.add_argument('--sign', help='Firma un fichero', metavar = 'fichero')

    parser.add_argument('--enc_sign', help='Cifra y firma un fichero', metavar = 'fichero')

    args = parser.parse_args()

    if args.create_id:
        users.create_id(args.create_id[0], args.create_id[1])

    elif args.search_id:
        users.search_id(args.search_id)

    elif args.delete_id:
        users.delete_id(args.delete_id)

    elif args.upload:
        if args.dest_id:
            nada()
            #files.upload(args.upload, args.dest_id)
        else:
            print("--upload necesita --dest_id")

    elif args.list_files:
        nada()
        #files.list_files()

    elif args.download: #TODO maybe logiquisimo ejemplos usan source_id? 
        nada()
        #files.download(args.download)

    elif args.delete_file:
        nada()
        #files.delete(args.delete_file)

    elif args.encrypt:
        if args.dest_id:
            publicKey = user.get_public_key(args.dest_id) 
            file = open(args.encrypt, "r")
            mensaje = file.read()
            crypto.encrypt(mensaje, publicKey)
        else:
            print("--encrypt necesita --dest_id")
    
    elif args.sign:
        file = open(args.sign, 'r')
        mensaje = file.read()
        crypto.sign(mensaje)

    elif args.enc_sign:
        if args.dest_id:
            file = open(args.sign, 'r')
            mensaje = file.read()
            publicKey = user.get_public_key(args.dest_id)
            crypto.enc_sign(mensaje, publicKey)
        else:
            print("--enc_sign necesita --dest_id")

def nada():
    return
