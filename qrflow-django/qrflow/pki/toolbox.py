import datetime

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


class CertificateHelper:

    @staticmethod
    def create_ca(
        country_name="BE",
        state_name="Brussels",
        locality_name="Brussels",
        organization_name="QR-Flow",
        common_name="qrflow.com",
        public_exponent=65537,
        key_size=4096,
        days=3650
    ):

        root_key = rsa.generate_private_key(
            public_exponent=public_exponent,
            key_size=key_size,
            backend=default_backend()
        )
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, country_name),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state_name),
            x509.NameAttribute(NameOID.LOCALITY_NAME, locality_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization_name),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ])
        root_cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            root_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=days)
        ).sign(root_key, hashes.SHA256(), default_backend())

        return root_key, root_cert

    @staticmethod
    def create_signed_certificate(
        root_key, root_cert,
        country_name="BE",
        state_name="Brussels",
        locality_name="Brussels",
        organization_name="QR-Flow",
        dsn_name="qrflow.com",
        public_exponent=65537,
        key_size=4096,
        days=365
    ):
        cert_key = rsa.generate_private_key(
            public_exponent=public_exponent,
            key_size=key_size,
            backend=default_backend()
        )
        new_subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, country_name),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state_name),
            x509.NameAttribute(NameOID.LOCALITY_NAME, locality_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization_name),
        ])
        cert = x509.CertificateBuilder().subject_name(
            new_subject
        ).issuer_name(
            root_cert.issuer
        ).public_key(
            cert_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=days)
        ).add_extension(
            x509.SubjectAlternativeName([x509.DNSName(dsn_name)]),
            critical=False,
        ).sign(root_key, hashes.SHA256(), default_backend())
        return cert_key, cert

    @staticmethod
    def to_public_pem(cert):
        return cert.public_bytes(serialization.Encoding.PEM)

    @staticmethod
    def to_private_pem(cert):
        return cert.private_bytes(
            serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

    @staticmethod
    def verify(cert, chain):
        try:
            # Return None or Raise an error
            chain.public_key().verify(
                data=cert.tbs_certificate_bytes,
                signature=cert.signature,
                padding=padding.PKCS1v15(),
                algorithm=hashes.SHA256()
            )
            return True
        except:
            return False


if __name__ == "__main__":
    root_key, root_cert = CertificateHelper.create_ca()

    with open("../../../media/ca.crt", "wb") as handler:
        handler.write(CertificateHelper.to_public_pem(root_cert))

    with open("../../../media/ca.key", "wb") as handler:
        handler.write(CertificateHelper.to_private_pem(root_key))

