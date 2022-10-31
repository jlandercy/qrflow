import io
import base64

import qrcode


def create_qrcode(payload: str):

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


def render_qrcode(payload: str, extension: str = "png", inline: bool = True):

    # Create QR Code:
    image = create_qrcode(payload)

    # Render QR Code:
    stream = io.BytesIO()
    image.save(stream, format=extension)

    if inline:
        stream = io.BytesIO(
            ("data:image/%s;base64, " % extension).encode() + base64.b64encode(stream.getvalue())
        )

    return stream
