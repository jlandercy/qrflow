import io
import re
import zlib

from pycose.messages import Sign1Message
from pycose.keys import CoseKey
from pycose.headers import Algorithm, KID
from pycose.algorithms import EdDSA
from pycose.keys.curves import Ed25519
from pycose.keys.keyparam import KpKty, OKPKpD, OKPKpX, KpKeyOps, OKPKpCurve
from pycose.keys.keytype import KtyOKP
from pycose.keys.keyops import SignOp, VerifyOp

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

import barcode
from barcode.writer import ImageWriter
import qrcode
import base45
import cbor2


class BarcodeHelper:

    @staticmethod
    def render(payload, class_name='ean13'):
        stream = io.BytesIO()
        factory = barcode.get_barcode_class(class_name)
        code = factory(payload, writer=ImageWriter(format="png"))
        code.write(stream)
        return stream


class QRCodeHelper:

    @staticmethod
    def create(payload):

        # Create QR Code:
        code = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        code.add_data(payload)
        code.make(fit=True)
        image = code.make_image(fill_color="black", back_color="white")

        return image

    @staticmethod
    def render(payload):
        stream = io.BytesIO()
        image = QRCodeHelper.create(payload)
        image.save(stream, format="png")
        return stream


class EPCHelper:

    @staticmethod
    def encode(
            bic="GKCCBEBB",
            name="Jean Landercy",
            iban="BE50063919771718",
            value=1.0,
            currency="EUR",
            reference="Support",
            information="QR-Flow Sample"
    ):
        return f"""BCD
001
1
SCT
{bic:}
{name:}
{iban:}
{currency:}{value:.2f}
CHAR
{reference:}
{information:}"""

    @staticmethod
    def decode(payload):
        raise NotImplemented


class DigitalGreenCertificateHelper:

    """

    References:
      - https://www.iana.org/assignments/cbor-tags/cbor-tags.xhtml
      - https://www.bartwolff.com/Blog/2021/08/08/decoding-the-eu-digital-covid-certificate-qr-code
      - https://github.com/ehn-dcc-development/eu-dcc-hcert-spec
      - https://pycose.readthedocs.io/en/latest/pycose/messages/sign1message.html
      - https://dx.dragan.ba/digital-covid-certificate/
      - https://pycose.readthedocs.io/en/latest/examples.html#cose-sign17
      - https://harrisonsand.com/posts/covid-certificates/
      - https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ed25519/
    """

    prefix_regex = re.compile("^([A-Z]{2}\d):")

    @staticmethod
    def get_header(key_id=b"kid"):
        return {Algorithm: EdDSA, KID: key_id}

    @staticmethod
    def create_key(public_key, private_key=None):

        operations = [VerifyOp]
        if private_key is None:
            private_key = b""
        else:
            operations += [SignOp]

        # https://pycose.readthedocs.io/en/latest/examples.html#cose-sign1
        return CoseKey.from_dict({
            KpKty: KtyOKP,
            OKPKpCurve: Ed25519,
            KpKeyOps: operations,
            OKPKpD: private_key,
            OKPKpX: public_key,
        })

    @staticmethod
    def create_new_key():

        # https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ed25519/
        private_key = Ed25519PrivateKey.generate()
        public_key = private_key.public_key()

        return DigitalGreenCertificateHelper.create_key(
            public_key=public_key._raw_public_bytes(),
            private_key=private_key._raw_private_bytes(),
        )

    @staticmethod
    def encode(data, protected_header=None, unprotected_header=None, key=None, prefix="HC1"):

        protected_header = protected_header or DigitalGreenCertificateHelper.get_header()
        unprotected_header = unprotected_header or {}
        key = key or DigitalGreenCertificateHelper.create_new_key()

        message = Sign1Message(
            phdr=protected_header,
            uhdr=unprotected_header,
            payload=cbor2.dumps(data),
            key=key
        )

        # Encode (CBOR -> ZLIB -> BASE45):
        decompressed = message.encode()
        compressed = zlib.compress(decompressed)
        b45data = base45.b45encode(compressed)
        payload = b45data.decode()

        # Prefix payload:
        if prefix:
            payload = prefix + ":" + payload

        return payload

    @staticmethod
    def decode(payload, key=None):

        prefix = None
        match = DigitalGreenCertificateHelper.prefix_regex.match(payload)
        if match:
            payload = DigitalGreenCertificateHelper.prefix_regex.sub("", payload)
            prefix = match.group(1)

        decoded = base45.b45decode(payload)
        decompressed = zlib.decompress(decoded)

        message = Sign1Message.decode(decompressed)
        message.key = key

        checked = key is not None
        if checked:
            verified = message.verify_signature()
        else:
            verified = False

        data = cbor2.loads(message.payload)

        return {
            "prefix": prefix,
            "protected_header": message.phdr,
            "unprotected_header": message.uhdr,
            "payload": data,
            "signature": message.signature,
            "checked": checked,
            "verified": verified,
        }

