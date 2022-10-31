import io
import base64

import qrcode


def create_qrcode(payload):

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


def render_qrcode(payload, inline=False):

    # Create QR Code:
    image = create_qrcode(payload)

    # Render QR Code:
    stream = io.BytesIO()
    image.save(stream)

    if inline:
        stream = io.BytesIO(b"data:image/png;base64," + base64.b64encode(stream.getvalue()))

    return stream
