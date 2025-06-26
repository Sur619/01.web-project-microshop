from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Generate RSA private key
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# Serialize the private key to PEM format
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)

# Serialize the private key and print it to confirm generation
print("Private Key:")
print(private_pem.decode())  # Decoding from bytes to string for better readability

# Generate the public key
public_key = private_key.public_key()

# Serialize the public key to PEM format
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

# Serialize the public key and print it to confirm generation
print("Public Key:")
print(public_pem.decode())  # Decoding from bytes to string for better readability

# Save the private and public keys to files
with open("../../certs/private_key.pem", "wb") as private_file:
    private_file.write(private_pem)

with open("../../certs/public_key.pem", "wb") as public_file:
    public_file.write(public_pem)

print("Private and Public keys generated successfully!")
