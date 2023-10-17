import io
import secrets
import zlib

from pycose.messages import Sign1Message
from pycose.keys import CoseKey
from pycose.headers import Algorithm, KID
from pycose.algorithms import EdDSA
from pycose.keys.curves import Ed25519
from pycose.keys.keyparam import KpKty, OKPKpD, OKPKpX, KpKeyOps, OKPKpCurve
from pycose.keys.keytype import KtyOKP
from pycose.keys.keyops import SignOp, VerifyOp

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
    def create(payload: str):

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

    """

    @staticmethod
    def get_default_header():
        return {Algorithm: EdDSA, KID: b'kid2'}

    @staticmethod
    def get_random_key():
        # Dummy key from https://pycose.readthedocs.io/en/latest/examples.html#cose-sign1
        return CoseKey.from_dict({
            KpKty: KtyOKP,
            OKPKpCurve: Ed25519,
            KpKeyOps: [SignOp, VerifyOp],
            OKPKpD: secrets.token_bytes(32),  # Private key
            OKPKpX: secrets.token_bytes(32),  # Public key
        })

    @staticmethod
    def encode(data, header=None, key=None, prefix="HC1"):

        header = header or DigitalGreenCertificateHelper.get_default_header()
        key = key or DigitalGreenCertificateHelper.get_random_key()

        message = Sign1Message(
            phdr=header,
            uhdr={},
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
    def decode(payload, key=None, prefix="HC1"):

        if prefix:
            payload = payload.replace(prefix + ":", "")

        decoded = base45.b45decode(payload)
        decompressed = zlib.decompress(decoded)

        message = Sign1Message.decode(decompressed)
        message.key = key

        if key is not None:
            check = message.verify_signature()
            print(check)

        data = cbor2.loads(message.payload)

        return data

    @staticmethod
    def sign(data, header=None, key=None):

        key = key or DigitalGreenCertificateHelper.get_random_key()
        header = header or DigitalGreenCertificateHelper.get_default_header()

        message = Sign1Message(
            phdr=header,
            uhdr={},
            payload=data,
            key=key
        )

        return message

    @staticmethod
    def verify(payload, key):
        message = Sign1Message.decode(payload)
        message.key = key
        return message.verify_signature()

