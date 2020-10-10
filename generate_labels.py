import timetap
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

key, secret = os.getenv('TIMETAP_API_KEY'), os.getenv('TIMETAP_PRIVATE_KEY')
client = timetap.Client(APIKey=key, PrivateKey=secret)
appointments = client.get_appointments_report(statusList=['OPEN'], pageSize=99999)

for app in appointments:
    emailAddress = app['client']['emailAddress']
    fullName = app['client']['fullName']
    dateOfBirth = app['client']['dateOfBirth']
    dob = dateOfBirth.split('-')
    dob2 = f'{dob[1]}/{dob[-1]}/{dob[0][-2:]}'
    # name_dob_img = qrcode.make(f'{fullName}\n{dob2}')
    # name_dob_img.save(f'codes/{fullName}_DOB_code.png')
    # email_img = qrcode.make(f'{emailAddress}')
    # email_img.save(f'codes/{fullName}_email_code.png')
    name_dob_img = qrcode.main.make(f'{fullName}\n{dob2}', version=1, box_size=1)
    email_img = qrcode.make(f'{emailAddress}', version=1, box_size=1)
    name_dob_img.save(f'codes/{fullName}_DOB_code.png')
    email_img.save(f'codes/{fullName}_email_code.png', version=1, box_size=1)