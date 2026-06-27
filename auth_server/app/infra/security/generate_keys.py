import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_keys():
    # Caminhos para salvar as chaves
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    resources_dir = os.path.join(base_dir, "resources")
    private_dir = os.path.join(resources_dir, "private")
    
    os.makedirs(private_dir, exist_ok=True)
    
    private_key_path = os.path.join(private_dir, "private_key.pem")
    public_key_path = os.path.join(resources_dir, "public_key.pem")
    
    print(f"Gerando chaves criptográficas em: {resources_dir}")
    
    # Gerar chave privada RSA 2048 bits
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    
    # Serializar chave privada para PEM
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Serializar chave pública para PEM
    public_key = private_key.public_key()
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Salvar chave privada
    with open(private_key_path, "wb") as f:
        f.write(pem_private)
    print(f"Chave privada salva em: {private_key_path}")
        
    # Salvar chave pública
    with open(public_key_path, "wb") as f:
        f.write(pem_public)
    print(f"Chave pública salva em: {public_key_path}")

if __name__ == "__main__":
    generate_keys()
