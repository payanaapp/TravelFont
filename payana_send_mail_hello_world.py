from __future__ import print_function

import base64

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import service_account

import mimetypes
import os
from email.message import EmailMessage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from payana.payana_bl.bigtable_utils.constants import bigtable_constants

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']


def authorize_gmail_client(credentials_path):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        # creds = creds.with_subject('tomhardy0503@gmail.com')
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


def gmail_send_message(credentials_file):
    """Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    # creds = service_account.Credentials.from_service_account_file(
    #                     credentials_file,
    #                     scopes=['https://www.googleapis.com/auth/gmail.send'])

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    impersonate = 'tomhardy0503@gmail.com'

    # creds = creds.with_subject(impersonate)

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        message.set_content('This is automated draft mail')

        message['To'] = 'payanaapp@gmail.com'
        message['From'] = 'tomhardy0503@gmail.com'
        message['Subject'] = 'Automated draft'

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }

        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message


def gmail_send_message_service_account(credentials_file, attachment_file):
    """Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    try:
        service = gmail_authorize_service_account(credentials_file)

        message = gmail_set_content(attachment_file)
        # message = gmail_set_payload(message, attachment_file)

        message['To'] = 'payanaapp@gmail.com'
        message['From'] = 'tomhardy0503@gmail.com'
        message['Subject'] = 'TravelFont Invitation'

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }

        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None

    return send_message


def gmail_authorize_service_account(credentials_file):

    try:
        creds = service_account.Credentials.from_service_account_file(
            credentials_file,
            scopes=['https://www.googleapis.com/auth/gmail.send'])

        impersonate = 'travelfont_admin@travelfont.com'

        creds = creds.with_subject(impersonate)
        service = build('gmail', 'v1', credentials=creds)
    except HttpError as error:
        print(F'An error occurred: {error}')
    except Exception as exc:
        print(str(exc))

    return service


def gmail_set_content(attachment_file):

    message = EmailMessage()
    message.set_content('Welcome to TravelFont')

    mime_message = gmail_set_payload(message, attachment_file)

    return mime_message


def gmail_set_payload(message, attachment_file):

    # guessing the MIME type
    type_subtype, _ = mimetypes.guess_type(attachment_file)
    maintype, subtype = type_subtype.split('/')

    with open(attachment_file, 'rb') as fp:
        attachment_data = fp.read()

    message.add_attachment(attachment_data, maintype, subtype)
    message.add_header('Content-Disposition', 'attachment',
                       filename=attachment_file)

    return message


def gmail_set_mime_payload(message, attachment_file):
    """Creates a MIME part for a file.

    Args:
      file: The path to the file to be attached.

    Returns:
      A MIME part that can be attached to a message.
    """
    content_type, encoding = mimetypes.guess_type(attachment_file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        with open(attachment_file, 'rb'):
            msg = MIMEText('r', _subtype=sub_type)
    elif main_type == 'image':
        print('image')
        with open(attachment_file, 'rb'):
            msg = MIMEImage('r', _subtype=sub_type)
    elif main_type == 'audio':
        with open(attachment_file, 'rb'):
            msg = MIMEAudio('r', _subtype=sub_type)
    else:
        with open(attachment_file, 'rb'):
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(attachment_file.read())
    attachment_filename = os.path.basename(attachment_file)
    msg.add_header('Content-Disposition', 'attachment',
                   filename=attachment_filename)

    # message.add_attachment(msg, main_type, sub_type)

    return msg


if __name__ == '__main__':
    # credentials_path = "/Users/abhinandankelgereramesh/Documents/payana_mail.json"
    # authorize_gmail_client(credentials_path)
    # gmail_send_message(credentials_path)
    service_credentials_path = os.path.join(
        bigtable_constants.travelfont_home, "google_mail_service_credentials.json")
    attachment_file = os.path.join(
        bigtable_constants.travelfont_home, "gmail_attach.jpg")
    gmail_send_message_service_account(
        service_credentials_path, attachment_file)
