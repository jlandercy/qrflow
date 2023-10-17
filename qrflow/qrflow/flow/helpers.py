import io
import zlib
from binascii import unhexlify, hexlify

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
    https://www.iana.org/assignments/cbor-tags/cbor-tags.xhtml
    https://www.bartwolff.com/Blog/2021/08/08/decoding-the-eu-digital-covid-certificate-qr-code
    https://github.com/ehn-dcc-development/eu-dcc-hcert-spec
    https://pycose.readthedocs.io/en/latest/pycose/messages/sign1message.html
    https://dx.dragan.ba/digital-covid-certificate/
    https://pycose.readthedocs.io/en/latest/examples.html#cose-sign1

    """

    @staticmethod
    def get_dummy_key():
        # Dummy key from https://pycose.readthedocs.io/en/latest/examples.html#cose-sign1
        cose_key = {
            KpKty: KtyOKP,
            OKPKpCurve: Ed25519,
            KpKeyOps: [SignOp, VerifyOp],
            OKPKpD: unhexlify(b'9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60'),
            OKPKpX: unhexlify(b'd75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a')
        }
        cose_key = CoseKey.from_dict(cose_key)
        return cose_key

    @staticmethod
    def encode(data, prefix="HC1"):
        cbortag = cbor2.CBORTag(18, [
            data["protected_header"],
            data["unprotected_header"],
            cbor2.dumps(data["payload"]),
            data["signature"],
        ])
        decompressed = cbor2.dumps(cbortag)
        compressed = zlib.compress(decompressed)
        b45data = base45.b45encode(compressed)
        payload = prefix + ":" + b45data.decode()
        return payload

    @staticmethod
    def decode(payload, prefix="HC1"):
        b45data = payload.replace(prefix + ":", "")
        decoded = base45.b45decode(b45data)
        decompressed = zlib.decompress(decoded)
        cbortag = cbor2.loads(decompressed)
        return {
            "protected_header": cbortag.value[0],
            "unprotected_header": cbortag.value[1],
            "payload": cbor2.loads(cbortag.value[2]),
            "signature": cbortag.value[3]
        }

    @staticmethod
    def sign(payload, key=None):

        key = key or DigitalGreenCertificateHelper.get_dummy_key()

        msg = Sign1Message(
            phdr={Algorithm: EdDSA, KID: b'kid2'},
            uhdr={},
            payload=payload,
            key=key
        )
        return {
            "protected_header": msg.phdr_encoded,
            "signature": msg.compute_signature()
        }
