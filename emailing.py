import smtplib
import imghdr
from email.message import EmailMessage

password = "kxsy mejq thbb bfsv"
SENDER = "andreusdinversions@gmail.com"
RECEIVER = SENDER

def send_email(image_path):
    print("send_email function started")
    email_message = EmailMessage()
    email_message["Subject"] = "New costumer showed up!"
    email_message.set_content("Hey, we just saw a new costumer!")

    with open(image_path, 'rb') as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image",
                                 subtype=imghdr.what(None, content))
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, password)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()
    print("send_email function ended")

