from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Cipher import PKCS1_OAEP
#result = json.dumps({'iv':iv, 'ciphertext':ct})
#TODO AES.CBC puede dar excepcion?

def encrypt(mensaje, clave_pub_r):
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
    iv = mensaje[0:16]
    sobre_digital = mensaje[16:16+256]

    # Obtenemos el sobre con OAEP
    # La clave es la privada del receptor
    cipher = PKCS1_OAEP.new(clave_priv_r)
    clave_s = cipher.decrypt(sobre_digital)

    cipher = AES.new(clave_s, AES.MODE_CBC, iv)
    mensaje_descifrado = unpad(cipher.decrypt(mensaje[16+256:]), AES.block_size)
    firma_digital = mensaje_descifrado[:256]
    mensaje_original = mensaje_descifrado[256:]

    # Hacemos hash256 del mensaje
    hash = SHA256.new(mensaje_original)

    #Comprobamos la firma_digital con el hash
    pkcs1_15.new(clave_pub_e).verify(hash, firma_digital)
    return mensaje_original


new_key = RSA.generate(2048)
public_key = new_key.publickey()
private_key = new_key
clave_pub_e=public_key
clave_priv_e=private_key
clave_pub_r=public_key
clave_priv_r=private_key
file= open("Prueba.txt","r")
mensaje=file.read()
encriptado= enc_sign(mensaje.encode("utf-8"),clave_priv_e ,clave_pub_r)
print(check_sign_and_decrypt(encriptado,clave_pub_e,clave_priv_r).decode("utf-8"))
