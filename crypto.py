from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Cipher import PKCS1_OAEP


def encrypt(mensaje, clave_pub_r):
    """
        Nombre: encrypt
        Descripcion: Funcion que encripta un mensaje mediante la AES con modo de encadenamiento CBC.
            Para ello crea una clave simetrica y un vector de inicializacion aleatorios. Genera
            el sobre digital de la clave.
        Argumentos:
            -mensaje: mensaje a cifrar.
            -clave_pub_r: clave publica del receptor.
        Retorno: IV + sobre digital + mensaje cifrado
    """
    print("-> Encriptando el mensaje...", end="")
    # Cifrado simétrico: AES con modo de encadenamiento CBC,
    # con IV de 16 bytes, y longitud de clave de 256 bits.
    # Generamos una clave de 256 bits = 32 bytes
    iv = get_random_bytes(16)
    clave_s = get_random_bytes(32)
    cipher = AES.new(clave_s, AES.MODE_CBC, iv)
    # El mensaje tiene que ser multiplo del tamanio del bloque
    # (16 en AES) asi que añadimos padding
    mensaje_cifrado = cipher.encrypt(pad(mensaje, AES.block_size))

    # Obtenemos el sobre con OAEP
    # La clave es clave_pub_r y el mensaje es clave_s
    cipher = PKCS1_OAEP.new(clave_pub_r)
    try:
        sobre_digital = cipher.encrypt(clave_s)
        print("OK")
        return iv + sobre_digital + mensaje_cifrado
    except ValueError:
        print("Error al cifrar.")
        return None


def sign(mensaje):
    """
        Nombre: sign
        Descripcion: Funcion que obtiene la firma de un mensaje mediante
            PCKS usando la clave privada del emisor (clave.pem).
        Argumentos:
            -mensaje: mensaje a firmar.
        Retorno: firma
    """
    print("-> Generando la firma...", end="")
    # Hacemos hash256 del mensaje
    h = SHA256.new(mensaje)
    # Ciframos con PKCS 1.5 el hash con la clave privada del emisor
    try:
        # Obtenemos la clave privada
        f = open('clave.pem', 'r')
        clave_priv_e = RSA.import_key(f.read())
        f.close()

        # sign puede generar ValueError y TypeError
        firma = pkcs1_15.new(clave_priv_e).sign(h)
        print("OK")
        return firma
    except (ValueError, TypeError):
        print("\nError al firmar.")
        return None


def enc_sign(mensaje, clave_pub_r):
    """
        Nombre: enc_sign
        Descripcion: Funcion que firma y cifra un mensaje en bytes.
        Argumentos:
            -mensaje: mensaje a firmar y cifrar
            -clave_pub_r: clave publica del receptor
        Retorno: mensaje firmado y cifrado
    """
    # Obtenemos la firma
    firma_digital = sign(mensaje)
    if firma_digital is None:
        return None

    # Ciframos la firma digital con el mensaje
    return encrypt(firma_digital + mensaje, clave_pub_r)


def decrypt(mensaje):
    """
        Nombre: decrypt
        Descripcion: Funcion que descifra un mensaje.
        Argumentos:
            -mensaje: mensaje cifrado y firmado
        Retorno: mensaje descifrado
    """
    # Obtenemos el vector de inicializacion y el sobre digital
    print("-> Descifrando fichero...", end="")
    iv = mensaje[0:16]
    sobre_digital = mensaje[16:16 + 256]

    # Obtenemos la clave privada del receptor
    f = open('clave.pem', 'r')
    clave_priv_r = RSA.import_key(f.read())
    f.close()

    # Obtenemos el sobre con OAEP
    cipher = PKCS1_OAEP.new(clave_priv_r)
    try:
        clave_s = cipher.decrypt(sobre_digital)
    except ValueError:
        print("Error: No es posible descifrar")
        return None

    # Desciframos y quitamos el pad
    cipher = AES.new(clave_s, AES.MODE_CBC, iv)
    mensaje_descifrado = unpad(cipher.decrypt(mensaje[16 + 256:]), AES.block_size)

    print("OK")
    return mensaje_descifrado


def check_sign(mensaje_descifrado, clave_pub_e):
    """
        Nombre: check_sign
        Descripcion: Funcion que comprueba la firma y obtiene el mensaje original.
        Argumentos:
            -mensaje: mensaje firmado
        Retorno: mensaje original
    """
    print("-> Verificando firma...", end="")

    firma_digital = mensaje_descifrado[:256]
    mensaje_original = mensaje_descifrado[256:]

    # Hacemos hash256 del mensaje
    h = SHA256.new(mensaje_original)

    # Comprobamos la firma_digital con el hash
    try:
        pkcs1_15.new(clave_pub_e).verify(h, firma_digital)
    except ValueError:
        print("Error al verificar la firma digital.")
        return None
    print("OK")
    return mensaje_original


def prueba_crypto():
    new_key = RSA.generate(2048)
    f = open('clave.pem', 'wb')
    f.write(new_key.export_key())
    f.close()
    public_key = new_key.publickey()
    encriptado = enc_sign("Hola mundo".encode('utf-8'), public_key)
    mensaje_descifrado = decrypt(encriptado)
    print(check_sign(mensaje_descifrado, public_key).decode("utf-8"))
