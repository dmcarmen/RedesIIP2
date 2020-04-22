import argparse
import files
import users
import crypto
import os

path_archivos = "Archivos/"
# TODO repasar prints y que a iris le funcione create_id

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interactúa con securebox')

    parser.add_argument('--create_id',
                        help='Crea una nueva identidad (par de claves púlica y privada) para un usuario con nombre '
                             'nombre y correo email, y la registra en SecureBox, para que pueda ser encontrada por '
                             'otros usuarios',
                        nargs=2, metavar=('Nombre', 'Email'))

    parser.add_argument('--search_id',
                        help='Busca un usuario cuyo nombre o correo electrónico contenga cadena en el repositorio de '
                             'identidades de SecureBox, y devuelve su ID',
                        metavar='Nombre/Email')

    parser.add_argument('--delete_id', help='Borra la identidad con ID id registrada en el sistema', metavar='id')

    parser.add_argument('--upload',
                        help='Envia un fichero a otro usuario, cuyo ID es especificado con la opción --dest_id',
                        metavar='fichero')

    parser.add_argument('--source_id', help='ID del emisor del fichero', metavar='id_emisor')

    parser.add_argument('--dest_id', help='ID del receptor del fichero', metavar='id_receptor')

    parser.add_argument('--list_files', action='store_true', help='Lista todos los ficheros pertenecientes al usuario')

    parser.add_argument('--download', help='Recupera un fichero con ID id_fichero del sistema', metavar='id_fichero')

    parser.add_argument('--delete_file', help='Borra un fichero del sistema', metavar='id_fichero')

    parser.add_argument('--encrypt',
                        help='Cifra un fichero, de forma que puede ser descifrado por otro usuario, cuyo ID es '
                             'especificado con la opción --dest_id',
                        metavar='fichero')

    parser.add_argument('--sign', help='Firma un fichero', metavar='fichero')

    parser.add_argument('--enc_sign', help='Cifra y firma un fichero', metavar='fichero')

    args = parser.parse_args()

    if args.create_id:
        users.create_id(args.create_id[0], args.create_id[1])

    elif args.search_id:
        users.search_id(args.search_id)

    elif args.delete_id:
        users.delete_id(args.delete_id)

    elif args.upload:
        if args.dest_id:
            files.upload(args.upload, args.dest_id)
        else:
            print("--upload necesita --dest_id")

    elif args.list_files:
        if args.source_id:
            files.list_files(args.source_id)
        else:
            print("--list_files necesita --source_id")

    elif args.download:
        if args.source_id:
            files.download(args.download, args.source_id)
        else:
            print("--download necesita --source_id")

    elif args.delete_file:
        files.delete(args.delete_file)

    elif args.encrypt:
        if args.dest_id:
            publicKey = users.get_public_key(args.dest_id)
            if publicKey is not None:
                file = open(args.encrypt, "r")
                mensaje = file.read()
                mensaje_cifrado = crypto.encrypt(mensaje, publicKey)
                if mensaje_cifrado is not None:
                    file_name = os.path.basename(args.encrypt)
                    f = open(path_archivos + "enc_" + file_name, "wb")
                    f.write(mensaje_cifrado)
                    f.close()
        else:
            print("--encrypt necesita --dest_id")

    elif args.sign:
        file = open(args.sign, 'r')
        mensaje = file.read()
        mensaje_firmado = crypto.sign(mensaje)
        if mensaje_firmado is not None:
            file_name = os.path.basename(args.sign)
            f = open(path_archivos + "sign_" + file_name, "wb")
            f.write(mensaje_firmado)
            f.close()

    elif args.enc_sign:
        if args.dest_id:
            file = open(args.enc_sign, 'r')
            mensaje = file.read()
            publicKey = users.get_public_key(args.dest_id)
            if publicKey is not None:
                mensaje_enc_sign = crypto.enc_sign(mensaje, publicKey)
                if mensaje_enc_sign is not None:
                    file_name = os.path.basename(args.enc_sign)
                    f = open(path_archivos + "enc_sign_" + file_name, "wb")
                    f.write(mensaje_enc_sign)
                    f.close()
        else:
            print("--enc_sign necesita --dest_id")
