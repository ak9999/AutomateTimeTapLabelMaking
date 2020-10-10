import timetap
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

if __name__ == "__main__":
    # Get TimeTap API key and secret from environment variables
    key, secret = os.getenv('TIMETAP_API_KEY'), os.getenv('TIMETAP_PRIVATE_KEY')
    # Initialize TimeTap API Client
    client = timetap.Client(APIKey=key, PrivateKey=secret)
    # Get all appointments
    appointments = client.get_appointments_report(statusList=['OPEN'], pageSize=99999)
    # Label dimensions
    label_width, label_height = 400, 66
    # Label text placement
    text_location = (70, 0)
    # Begin processing appointments to get patient information.
    for app in appointments:
        emailAddress = app['client']['emailAddress']
        fullName = app['client']['fullName']
        dateOfBirth = app['client']['dateOfBirth']
        dob = dateOfBirth.split('-')  # Split the date of birth.
        dob2 = f'{dob[1]}/{dob[-1]}/{dob[0][-2:]}'  # MM/DD/YY
        # Create QR Codes
        name_dob_img = qrcode.main.make(f'{fullName}\n{dob2}', version=None, box_size=2)
        email_img = qrcode.make(f'{emailAddress}', version=None, box_size=2)
        qr_width, qr_height = name_dob_img.size  # QR Codes are same size, use arbitrary code.
        # Create the 1st label for name and date of birth
        name_dob_label = Image.new('RGBA', (label_width, label_height), (255, 255, 255, 255))  # Make a new image for the label
        background_width, background_height = name_dob_label.size
        offset = ((background_height - qr_height) // 2, (background_height - qr_height) // 2)
        name_dob_label.paste(name_dob_img, offset)
        # Draw text onto label
        draw = ImageDraw.Draw(name_dob_label)
        # Choose font and font size
        font = ImageFont.truetype('resources/SourceCodePro-Medium.ttf', 14)
        draw.text(text_location, f'{fullName}\n{dob2}', (0, 0, 0), font=font)  # Write text
        name_dob_label.save(f'codes/{fullName}_DOB_code.png')  # Save image
        # Repeat the above for the email address label.
        email_address_label = Image.new('RGBA', (label_width, label_height), (255, 255, 255, 255))  # Make a new image for the label
        email_address_label.paste(email_img, offset)
        draw = ImageDraw.Draw(email_address_label)  # Draw text onto label
        draw.text(text_location, f'{emailAddress}', (0, 0, 0), font=font)  # Write text
        email_address_label.save(f'codes/{fullName}_email_code.png')
