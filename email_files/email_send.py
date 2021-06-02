import boto3
from botocore.exceptions import ClientError
import itertools
from email_structure import BODY_HTML
from email_config import emails_to, emails_from, SENDER, SUBJECT, BODY_TEXT, CHARSET

def config_email():
    """ set up the default parameters and connection to ses """
    AWS_REGION = "us-east-2"
    client = boto3.client('ses',region_name=AWS_REGION)
    return client

def email_verification(emails_to, emails_from, ses):
    """ ensure that all emails have been verified, print those already verified """
    response = ses.list_identities(
            IdentityType = 'EmailAddress'
        )
    # if email verified, add to verified list, else send verification email
    verified_emails = []
    for email_to, email_from in itertools.zip_longest(emails_to,emails_from):
        if email_to in (response.get('Identities')):
            verified_emails.append(email_to)
        if email_from in (response.get('Identities')):
            verified_emails.append(email_from)
        elif email_to and email_to not in (response.get('Identities')):
            ses.verify_email_address(
                EmailAddress = email_to
            )
        elif email_from and email_from not in (response.get('Identities')):
            ses.verify_email_address(
                EmailAddress = email_from
            )
    print(f'Verified emails include: {verified_emails} \n')

def send_email():
    """ Try to send the email to recipients using SES """
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': RECIPIENT
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


# emails recpipients and sender address to be used for verification and sending email
client = config_email()
email_verification(emails_to, emails_from, client)
RECIPIENT = emails_to

# Comment to stop sending emails
send_email()