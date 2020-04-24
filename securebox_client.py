import argparse
import files
import users
import crypto
import utils as u
import os


if __name__ == "__main__":
    # Guardamos el token, el header para todas las peticiones y el path de archivos
    # Estas variables están en utils
    u.config_ini()
    u.headers['Authorization'] = "Bearer " + u.token

    # Si el token existe continuamos
    if u.token != "":

        # Añadimos todos los posibles argumentos al parser
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

        parser.add_argument('--enc_sign', help='Cifra y firma un fichero para --dest_id', metavar='fichero')

        parser.add_argument('--dec_check', help='Desencripta y valida la firma de un fichero de --source_id', metavar='fichero')

        args = parser.parse_args()

        # Se realiza la accion correspondiente segun los argumentos
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

        # Para encriptar pedimos la clave publica del destinatario, ciframos
        # y guardamos el fichero encriptado en path_archivos
        elif args.encrypt:
            if args.dest_id:
                publicKey = users.get_public_key(args.dest_id)
                if publicKey is not None:
                    try:
                        f = open(args.encrypt, "rb")
                        mensaje_cifrado = crypto.encrypt(f.read(), publicKey)
                        f.close()
                        # Si se ha cifrado correctamente lo guardamos como: enc_ + nombre del fichero
                        if mensaje_cifrado is not None:
                            file_name = os.path.basename(args.encrypt)
                            f = open(u.path_archivos + "enc_" + file_name, "wb")
                            f.write(mensaje_cifrado)
                            f.close()
                    except FileNotFoundError:
                        print("El archivo no existe")
            else:
                print("--encrypt necesita --dest_id")

        # Firmamos un fichero y la guardamos en path_archivos
        elif args.sign:
            try:
                f = open(args.sign, 'rb')
                mensaje = f.read()
                firma_digital = crypto.sign(mensaje)
                f.close()
                # Si se ha firmado correctamente guardamos la firma y el mensaje como: sign_ + nombre del fichero
                if firma_digital is not None:
                    file_name = os.path.basename(args.sign)
                    f = open(u.path_archivos + "sign_" + file_name, "wb")
                    f.write(firma_digital + mensaje)
                    f.close()

            except FileNotFoundError:
                print("El archivo no existe")

        # Encripta y frima un archivo para un destinatario y lo guarda en path_archivos
        elif args.enc_sign:
            if args.dest_id:
                try:
                    f = open(args.enc_sign, 'rb')
                    mensaje = f.read()
                    f.close()
                    publicKey = users.get_public_key(args.dest_id)
                    if publicKey is not None:
                        mensaje_enc_sign = crypto.enc_sign(mensaje, publicKey)
                        # Si se ha realizado correctamente lo guardarmos como: enc_sign_ + nombre del fichero
                        if mensaje_enc_sign is not None:
                            file_name = os.path.basename(args.enc_sign)
                            f = open(u.path_archivos + "enc_sign_" + file_name, "wb")
                            f.write(mensaje_enc_sign)
                            f.close()
                except FileNotFoundError:
                    print("El archivo no existe")
            else:
                print("--enc_sign necesita --dest_id")

        # Desencripta y comprueba la firma de un fichero dado. Guarda el fichero
        # dado en path_archivos
        elif args.dec_check:
            if args.source_id:
                try:
                    f = open(args.dec_check, 'rb')
                    mensaje = f.read()
                    f.close()
                    mensaje_descifrado = crypto.decrypt(mensaje)
                    publicKey = users.get_public_key(args.source_id)
                    if publicKey is not None:
                        check = crypto.check_sign(mensaje_descifrado, publicKey)
                        print("La firma es ", end = "")
                        if check is None:
                            print("incorrecta")
                        else:
                            print("correcta")
                            file_name = os.path.basename(args.dec_check)
                            f = open(u.path_archivos + "dec_check_" + file_name, "wb")
                            f.write(check)
                            f.close()
                except FileNotFoundError:
                    print("El archivo no existe")
            else:
                print("--dec_check necesita --source_id")

        else:
            print("Introduce --help para ver los posibles comandos")
    else:
        print("No hay token.")
