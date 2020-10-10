import qrcode
from PIL import Image, ImageDraw, ImageFont

# qr = qrcode.QRCode(version=1, box_size=1)
# qr.add_data('Name: AJ\nSpecial Skill: Exist')
# img = qr.make_image(fill_color='black', back_color='white')
# img.save('code.png')

# Two-liner:
# bitmap = qrcode.main.make('Abdullah Khan made this image in two lines!', version=1, box_size=1)
# bitmap.save('sample.png')

# Define color tuple
background_white = (255, 255, 255, 255)
foreground_black = (0, 0, 0)

# Create QR Code
full_name = 'John Doe'
date_of_birth = '06/17/89'
email_address = 'john.doe.very.long.email.address@gmail.com'
# qr_code1 = qrcode.main.make(f'{full_name}\n{date_of_birth}', version=None, box_size=1)
# qr_code1.save('samples/sample1.png')
qr_code2 = qrcode.main.make(f'{full_name}\n{date_of_birth}', version=None, box_size=2)
qr_code2.save('samples/sample2.png')
# qr_code3 = qrcode.main.make(f'{full_name}\n{date_of_birth}', version=None, box_size=3)
# qr_code3.save('samples/sample3.png')
# qr_code4 = qrcode.main.make(f'{full_name}\n{date_of_birth}', version=None, box_size=4)
# qr_code4.save('samples/sample4.png')
# qr_code5 = qrcode.main.make(f'{full_name}\n{date_of_birth}', version=None, box_size=5)
# qr_code5.save('samples/sample5.png')
# qr_code6 = qrcode.main.make(f'{full_name}\n{date_of_birth}', version=None, box_size=6)
# qr_code6.save('samples/sample6.png')

email_address_code2 = qrcode.main.make(f'{email_address}', version=None, box_size=2)
email_address_code2.save('samples/email_address2.png')

# Open the QR Code for reading
# qr_img = Image.open('sample.png', mode='r')
# qr_width, qr_height = qr_img.size
qr_width, qr_height = qr_code2.size
# label = Image.new('RGBA', (400, 66), (255, 255, 255, 255))  # Make a new image for the label
# background_width, background_height = label.size
# offset = ((background_height - qr_height) // 2, (background_height - qr_height) // 2)
# label.paste(qr_code2, offset)

# draw = ImageDraw.Draw(label)
# font = ImageFont.truetype('resources/SourceCodePro-Medium.ttf', 12)
# draw.text((70, 0), f'{full_name}\n{date_of_birth}', (0, 0, 0), font=font)
# label.save('label.png')

label = Image.new('RGBA', (400, 150), background_white)
background_width, background_height = label.size
label.paste(qr_code2, (0, 0))
label.paste(email_address_code2, (0, 75))
draw = ImageDraw.Draw(label)
font = ImageFont.truetype('resources/SourceCodePro-Medium.ttf', 12)
draw.text((90, 0), f'{full_name}\n{date_of_birth}', foreground_black, font=font)
draw.text((90, 85), f'{email_address}', foreground_black, font=font)
# label.show()
label.save('samples/double_label.png')
