import Crypto
#result = json.dumps({'iv':iv, 'ciphertext':ct})
#TODO AES.CBC puede dar excepcion?

def encrypt(mensaje, clave_pub_r):
    # Cifrado simétrico: AES con modo de encadenamiento CBC,
    # con IV de 16 bytes, y longitud de clave de 256 bits.
    # Generamos una clave de 256 bits
    iv = get_random_bytes(16)
    clave_s = get_random_bytes(256)
    cipher = AES.new(clave_s, AES.MODE_CBC, iv)
    # El mensaje tiene que ser multiplo del tamanio del bloque
    # (16 en AES) asi que añadimos padding
    mensaje_cifrado = cipher.encrypt(pad(mensaje, AES.block_size))

    # Obtenemos el sobre con OAEP
    # La clave es clave_pub_r y el mensaje es clave_s
    cipher = PKCS1_OAEP.new(clave_pub_r)
    try:
        sobre_digital = cipher.encrypt(clave_s)
        return iv + sobre_digital + mensaje_cifrado
    except(ValueError):
        return None

def sign(mensaje, clave_priv_e):
    # Hacemos hash256 del mensaje
    hash = SHA256.new(mensaje)
    # Ciframos con PKCS 1.5 el hash con la clave privada del emisor
    try:
        # sign raises ValueError y TypeError
        firma_digital = pkcs1_15.new(clave_priv_e).sign(hash)
        return firma_digital
    except (ValueError, TypeError):
        return None

def enc_sign(mensaje, clave_priv_e, clave_pub_r):
    firma_digital = sign(mensaje, clave_priv_e)

    mensaje_enc_sign = encrypt(firma_digital + mensaje, clave_pub_r)

    return mensaje_enc_sign

def check_sign_and_decrypt(mensaje, clave_pub_e, clave_priv_r):
    #TODO se coge la parte del mensaje que corresponde?
    iv = mensaje[0:16]
    sobre_digital = mensaje[16:16+clave_priv_r[1]] #TODO_1 tan grande como n
    try:
        # Obtenemos el sobre con OAEP
        # La clave es la privada del receptor
        cipher = PKCS1_OAEP.new(clave_priv_r)
        clave_s = cipher.decrypt(sobre_digital)

        cipher = AES.new(clave_s, AES.MODE_CBC, iv)
        mensaje_descifrado = cipher.decrypt(mensaje[16+clave_priv_r[1]:]) #TODO_1

        firma_digital = mensaje_descifrado[:clave_pub_e[1]] #TODO tan larga como modulo rsa,es decir, n
        mensaje_original = mensaje_descifrado[]

        # Hacemos hash256 del mensaje
        hash = SHA256.new(mensaje_original)
        #Comprobamos la firma_digital con el hash
        pkcs1_15.new(clave_pub_e).verify(hash, firma_digital)
        return mensaje_original

    except(ValueError, TypeError):
        return None
