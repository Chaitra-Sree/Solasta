# qr_generate.py
import qrcode
import os

# Define the URL of your order page
order_page_url = "http://127.0.0.1:8000/"  # Replace with your actual URL

# Generate the QR code
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(order_page_url)
qr.make(fit=True)

# Save the QR code image in the static/images directory
output_dir = os.path.join('static', 'images')
os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
qr_image = qr.make_image(fill="black", back_color="white")
qr_image.save(os.path.join(output_dir, "qr_code.png"))

print("QR Code generated and saved ")

