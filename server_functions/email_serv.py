import imaplib
import email
import time
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_facebook_registration_code(user_email):
    email_address = os.getenv('EMAIL_ADDRESS')
    password = os.getenv('EMAIL_PASSWORD')
    imap_server = os.getenv('IMAP_SERVER')

    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_address, password)

    # Search for emails from Facebook
    for _ in range(10):  # Try for 5 minutes (10 * 30 seconds)
        _, search_data = mail.search(None,
                                     'FROM', '"@facebookmail.com"',
                                     'TO', f'"{user_email}"'
                                     'UNSEEN')
        for num in search_data[0].split():
            _, data = mail.fetch(num, '(RFC822)')
            email_body = data[0][1]
            message = email.message_from_bytes(email_body)

            if message.is_multipart():
                for part in message.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        code_match = re.search(r'\b\d{6}\b', body)
                        if code_match:
                            return code_match.group(0)
            else:
                body = message.get_payload(decode=True).decode()
                code_match = re.search(r'\b\d{6}\b', body)
                if code_match:
                    return code_match.group(0)

        time.sleep(30)  # Wait 30 seconds before checking again

    return None