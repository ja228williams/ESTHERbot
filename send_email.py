import smtplib
import ssl
import traceback
from email.message import EmailMessage


def send_email(sender_gmail, password, message, receiver, subject=None):
    """
    Sends an email from one account to another.

    :param sender_gmail: Sending account of the email being delivered
    :param password: Password for the email account being used to send the update email.
    :param message: Message sent in the email
    :param receiver: Receiving account of the email being delivered
    :param subject: Subject of the email
    """
    port = 465
    context = ssl.create_default_context()
    print("\ncontext created...")

    try:
        print("setting up server...")
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_gmail, password)
            print("logged in...")

            # creates EmailMessage object
            e_message = EmailMessage()
            e_message.set_content(message)
            e_message['From'] = sender_gmail
            e_message['To'] = receiver
            e_message['Subject'] = subject

            server.send_message(e_message)
            print("email sent successfully")

    except:
        print("\nError sending email:")
        print(traceback.format_exc())
