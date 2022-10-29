import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

import qrcode


#Generate Key Pair:
def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open('../../secrets/private.pem', 'wb') as f:
        f.write(private_pem)

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open('../../secrets/public.pem', 'wb') as f:
        f.write(public_pem)


def load_key_pair():
    with open("../../secrets/private.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    with open("../../secrets/public.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return private_key, public_key


def sign(message, key):
    
    # Encode if necessary
    if isinstance(message, str):
        message = message.encode()

    # Prehash:
    digest = hashes.Hash(hashes.SHA256())
    digest.update(message)
    prehash = digest.finalize()

    # Sign:
    signature = key.sign(
        prehash,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    return signature


def generate_qrcode(message):
    code = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    code.add_data(message)
    code.make(fit=True)
    image = code.make_image(fill_color="black", back_color="white")
    return image


if __name__ == "__main__":

    #generate_key_pair()
    
    private, public = load_key_pair()
    print(private, public)
    
    signed = sign("Blue forks are evil.", private)
    print(signed)

    image = create_qrcode("F0205-BeeOLab-DNA-2022/P3-1")
    with open("../../media/test.png", "wb") as handler:
        image.save(handler)
    
