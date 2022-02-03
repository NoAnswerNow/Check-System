import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from auth_data import passw, mail


def send_email() :
    attachment = "check_system.txt"
    msg = MIMEMultipart()
    msg['Subject'] = "Report"
    msg['From'] = mail
    msg['To'] = mail
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(attachment, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename=attachment)
    msg.attach(part)
    with smtplib.SMTP('smtp.gmail.com',587) as server:
       server.ehlo()
       server.starttls()
       server.ehlo()
       server.login(mail, passw)
       server.send_message(msg)
       server.quit()