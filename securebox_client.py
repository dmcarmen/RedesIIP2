import Crypto
#result = json.dumps({'iv':iv, 'ciphertext':ct})

def encrypt(mensaje, clave_pub_r):
    # Cifrado simétrico: AES con modo de encadenamiento CBC,
    # con IV de 16 bytes, y longitud de clave de 256 bits.
    # Generamos una clave de 256 bits
    iv = get_random_bytes(16)
    clave_s = get_random_bytes(256)
    cipher = AES.new(clave_S, AES.MODE_CBC, iv)
    # El mensaje tiene que ser multiplo del tamanio del bloque
    # (16 en AES) asi que añadimos padding
    mensaje_cifrado = cipher.encrypt(pad(mensaje, AES.block_size))

    # Obtenemos el sobre con OAEP
    # La clave es clave_pub_r y el mensaje es clave_s
    cipher = PKCS1_OAEP.new(clave_pub_r)
    sobre_digital = cipher.encrypt(clave_s)

    return iv + sobre_digital + mensaje_cifrado

def sign(mensaje, clave_priv_e):
    # Hacemos hash256 del mensaje
    hash = SHA256.new(mensaje)
    # Ciframos con PKCS 1.5 el hash con la clave privada del emisor
    firma_digital = pkcs1_15.new(clave_priv_e).sign(hash)

    return firma_digital

def enc_sign(mensaje, clave_priv_e, clave_pub_r):
    firma_digital = sign(mensaje, clave_priv_e)

    mensaje_enc_sign = encrypt(firma_digital + mensaje, clave_pub_r)

    return mensaje_enc_sign
