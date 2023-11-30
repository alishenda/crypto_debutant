import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# Génération et stockage des clés
def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

# Chiffrement du message
def encrypt_message(message, public_key):
    # Chiffrement AES du message
    key = os.urandom(32)  # Clé AES
    iv = os.urandom(16)  # Vecteur d'initialisation AES
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()
    encrypted_message = encryptor.update(padded_data) + encryptor.finalize()

    # Chiffrement RSA de la clé AES
    encrypted_key = public_key.encrypt(
        key,
        rsa_padding.OAEP(
            mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted_message, iv, encrypted_key

# Déchiffrement du message
def decrypt_message(encrypted_message, iv, encrypted_key, private_key):
    # Déchiffrement RSA de la clé AES
    key = private_key.decrypt(
        encrypted_key,
        rsa_padding.OAEP(
            mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Déchiffrement AES du message
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(128).unpadder()
    padded_message = decryptor.update(encrypted_message) + decryptor.finalize()
    decrypted_message = unpadder.update(padded_message) + unpadder.finalize()

    return decrypted_message.decode()

# Exemple d'utilisation
alice_private_key, alice_public_key = generate_keys()
bob_private_key, bob_public_key = generate_keys()

# Alice envoie un message à Bob
message = "Bonjour Bob!"
encrypted_message, iv, encrypted_key = encrypt_message(message, bob_public_key)

# Bob reçoit et déchiffre le message
decrypted_message = decrypt_message(encrypted_message, iv, encrypted_key, bob_private_key)
print("Message reçu par Bob:", decrypted_message)