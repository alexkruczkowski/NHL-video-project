""" file for storing email parameters """
from datetime import datetime, timedelta

# recpipient and sender email addresses
emails_to = ["ak.kruczkowski@gmail.com", "a.kruczkowski@yahoo.ca"]
emails_from = ["nhl.video.recap@gmail.com"]

# Replace sender@example.com with your "From" address.
# This address must be verified with Amazon SES.
SENDER = f"NHL Video Recaps <{emails_from[0]}>"

# get yesterday's date for use in the subject
yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

# The subject line for the email.
SUBJECT = f"NHL video recap for {yesterday}"

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("NHL Video Recap email\r\n"
             "If you are reading this then the HTML did not load correctly "
             "please get in touch with us if you are experiencing this issue"
            )
            
# The character encoding for the email.
CHARSET = "UTF-8"