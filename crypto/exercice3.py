from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization

# Génération de paires de clés pour signature numérique
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

print("Clé Privée pour Signature Numérique:\n", private_key_pem.decode())
print("Clé Publique pour Signature Numérique:\n", public_key_pem.decode())

# Signature d'un message avec la clé privée
message = "Message à signer."
message_bytes = message.encode('utf-8')

signature = private_key.sign(
    message_bytes,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

print("Signature du Message:", signature)

# Vérification de la signature avec la clé publique
try:
    public_key.verify(
        signature,
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    verification_result = "La signature est valide."
except Exception as e:
    verification_result = "La signature n'est pas valide."

print("Résultat de la Vérification de la Signature:", verification_result)
