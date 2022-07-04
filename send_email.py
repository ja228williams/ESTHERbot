import smtplib
import ssl
import traceback
from email.message import EmailMessage
import sys

# login credentials
my_password = ""


def send_email(sender_gmail, password, message, receiver, subject=None):
    port = 465
    context = ssl.create_default_context()
    print("\ncontext created...")

    try:
        print("setting up server...")
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_gmail, password)
            print("logged in...")

            e_message = EmailMessage()
            e_message.set_content(message)
            e_message['From'] = sender_gmail
            e_message['To'] = receiver
            e_message['Subject'] = subject

            server.send_message(e_message)
            print("email sent successfully")
    except Exception as e:
        print("\nError sending email:")
        print(traceback.format_exc())


# try sending to myself first? could get around credential issues, esp with rice email
# print(send_email("jaw15developer@gmail.com", my_password, "peter", "jaw15@rice.edu"))
