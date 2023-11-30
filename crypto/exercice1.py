from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

# Génération de la clé symétrique
key = os.urandom(32)  # Génération d'une clé de 32 octets pour AES-256
print("Clé Symétrique Générée:", key)

# Chiffrement d'un message
# Pour la démonstration, nous utilisons un message prédéfini
message = "Ceci est un message secret."
message_bytes = message.encode('utf-8')

# Préparation du chiffrement AES
backend = default_backend()
cipher = Cipher(algorithms.AES(key), modes.CBC(os.urandom(16)), backend=backend)
encryptor = cipher.encryptor()

# Padding du message
padder = padding.PKCS7(128).padder()
padded_data = padder.update(message_bytes) + padder.finalize()

# Chiffrement du message
ct = encryptor.update(padded_data) + encryptor.finalize()
print("Message Chiffré:", ct)

# Déchiffrement du message
decryptor = cipher.decryptor()
pt = decryptor.update(ct) + decryptor.finalize()

# Suppression du padding
unpadder = padding.PKCS7(128).unpadder()
decrypted_message = unpadder.update(pt) + unpadder.finalize()
print("Message Déchiffré:", decrypted_message.decode('utf-8'))

