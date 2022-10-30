import io
import base64

import qrcode


def create_qrcode(message, inline=False):

    # Create QR Code:
    code = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    code.add_data(message)
    code.make(fit=True)
    image = code.make_image(fill_color="black", back_color="white")

    # Render QR Code:
    stream = io.BytesIO()
    image.save(stream)

    if inline:
        stream = io.BytesIO(b"data:image/png;base64," + base64.b64encode(stream.getvalue()))

    return stream

