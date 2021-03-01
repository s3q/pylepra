import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import os

class Sendmail:

    def __init__(self, sender_email, password):
        self.sender_email = str(sender_email).strip()  # <---- write your email
        self.password = str(password).strip()  # <---- write password

        # <--- receiver email : 
        self.receiver_email = input("Type receiver email and press enter : ")
        # <---- messsage subject :
        self.subject = input("Type message subject and press enter : ").strip()
        # <---- message content (Html) :
        self.content = input(
            "Type message content and press enter : \n").strip()

    def preparation(self):
        # check for emails and password :
        if not re.match("[^@]+@[^@]+\.[^@]+", self.receiver_email) and not re.match("[^@]+@[^@]+\.[^@]+", self.sender_email) and self.password != "":
            print("invalid email .!")
            return False
        else:
            return True

    def send(self):
        #
        if self.preparation():
            try:
                # manages a connection to an SMTP or ESMTP server
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    # Puts the connection to the SMTP server into TLS mode :
                    server.starttls()

                    #
                    if not server.login(self.sender_email, self.password):
                        print("Failed to login .!")
                    else:

                        message = MIMEMultipart("alternative")
                        message["From"] = self.sender_email
                        message["To"] = self.receiver_email
                        message["Subject"] = self.subject

                        # <---- Class for generating text/* type MIME documents
                        htmlPart = MIMEText(self.content, 'html')

                        # <---- Add the given payload to the current payload
                        message.attach(htmlPart)

                        print("loading ...")

                        #
                        if server.sendmail(self.sender_email, self.receiver_email, message.as_string()):
                            print("The email has been sent successfully .")

                    # Terminate the SMTP session :
                    server.quit()
            except:
                print("Something is wrong .!")


sendmail = Sendmail("", # --> your account
                    "" # ---> password
                    )
sendmail.preparation()
sendmail.send()

