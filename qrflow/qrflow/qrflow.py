import qrcode


def create_qrcode(message):
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

    image = create_qrcode("Some Identifier you want to scan")
    with open("../../media/test.png", "wb") as handler:
        image.save(handler)
