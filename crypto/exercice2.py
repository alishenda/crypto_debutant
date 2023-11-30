from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding as rsa_padding
from cryptography.hazmat.primitives import hashes

# Génération de paires de clés RSA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

public_key = private_key.public_key()

# Affichage des clés générées
private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

print("Clé Privée RSA:\n", private_key_pem.decode())
print("Clé Publique RSA:\n", public_key_pem.decode())

# Chiffrement d'un message avec la clé publique RSA
# Note: Dans une application réelle, le message serait saisi par l'utilisateur.
message = "Ceci est un message confidentiel."
message_bytes = message.encode('utf-8')

encrypted_message = public_key.encrypt(
    message_bytes,
    rsa_padding.OAEP(
        mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Message Chiffré:", encrypted_message)

# Déchiffrement du message avec la clé privée RSA
decrypted_message = private_key.decrypt(
    encrypted_message,
    rsa_padding.OAEP(
        mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Message Déchiffré:", decrypted_message.decode('utf-8'))