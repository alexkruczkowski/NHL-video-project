import smtplib
import os
import imghdr
from email.message import EmailMessage
import pandas as pd
from email_structure import structure

# get email info from environment variables
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

# info for sending email via SMTP
msg = EmailMessage()
msg['Subject'] = 'NHL Recap from Last Night'
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'ak.kruczkowski@gmail.com'

msg.set_content('If you are seeing this, the HTML below may not have loaded correctly')

# set message HTML formatting
msg.add_alternative(structure, 
subtype='html')

# send email message via SMTP
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)

