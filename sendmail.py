
import smtplib
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart


#to be put in environment variables 
SENDER_EMAIL='omr@cse.iitm.ac.in'
SENDER_PASSWORD='wzxy vgmz wloo gape'
SMTP_SERVER_URI='smtp.gmail.com'

# Email server configuration
sender_email = SENDER_EMAIL
sender_password = SENDER_PASSWORD
smtp_server_uri = SMTP_SERVER_URI
smtp_port = 587
   

def profiler_error_mail():
        receiver_email = 'omr@cse.iitm.ac.in'
        subject = (
            "MASTER ALERT!! ERROR!- An error has been thrown, "
            "Please look into it immediately!!"
        )
        body = (
            "The profiler has crashed and it not automatically recoverable by the system\n"
            "Please look into it immediately.\n\n"
            "OpenMalwareResearch sysmaster"
        )

        try:
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = subject
            message.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(smtp_server_uri, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, message.as_string())
                print(f"Successfully mailed to {receiver_email}")

        except Exception as e:
                print(f"There is an error in the email script: {e}")
