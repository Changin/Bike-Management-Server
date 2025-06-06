import qrcode
import os


def generate_qr_code(data: str, filename: str = "qr_code.png", output_dir: str = "media/qrcodes") -> str:
    if not data:
        raise ValueError("QR 코드에 담을 데이터가 비어 있습니다.")

    os.makedirs(output_dir, exist_ok=True)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    file_path = os.path.join(output_dir, filename)
    img.save(file_path)

    return file_path
