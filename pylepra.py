import random
import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import os
import json

from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class Maillepra:

    def __init__(self, sender_email, password):
        self.sender_email = str(sender_email).strip()  # <---- write your email
        self.password = str(password).strip()  # <---- write password

    def preparationforsendemail(self):

        # <--- receiver email : salimalsulaimi204@gmail.com
        self.receiver_email = input(
            "@ - Type receiver email and press enter : ")
        # <---- messsage subject
        self.subject = input(
            "@ - Type message subject and press enter : ").strip()
        # <---- message content (Html)
        self.content = input(
            "@ - Type message content and press enter : \n").strip()

        # check for emails and password :
        if not re.match("[^@]+@[^@]+\.[^@]+", self.receiver_email) and not re.match("[^@]+@[^@]+\.[^@]+", self.sender_email) and self.password != "":
            print(" - Invalid email .!")
            return False
        else:
            return True

    def sendemail(self):
        #
        if self.preparationforsendemail():
            try:
                # manages a connection to an SMTP or ESMTP server
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    # Puts the connection to the SMTP server into TLS mode :
                    server.starttls()

                    #
                    if not server.login(self.sender_email, self.password):
                        print(" - Failed to login .!")
                    else:

                        message = MIMEMultipart("alternative")
                        message["From"] = self.sender_email
                        message["To"] = self.receiver_email
                        message["Subject"] = self.subject

                        # <---- Class for generating text/* type MIME documents
                        htmlPart = MIMEText(self.content, 'html')

                        # <---- Add the given payload to the current payload
                        message.attach(htmlPart)

                        print(" - Loading ...")

                        #
                        if server.sendmail(self.sender_email, self.receiver_email, message.as_string()):
                            print(" - The email has been sent successfully .")

                    # Terminate the SMTP session :
                    server.quit()
            except:
                print(" - Something is wrong .!")

    def getinbox(self):

        print(" - GET EMIAL ...")

        imap = imaplib.IMAP4_SSL("imap.gmail.com")

        imap.login(self.sender_email, self.password)

        # select inbox
        print(" - Select inbox ...")
        statustext, messagesb = imap.select("INBOX")

        # number of top emails to fetch
        # numberemailfetch = 1
        numberemailfetch = int(input("@ - Type email index : ").strip())

        # total number of emails
        messagescount = int(messagesb[0])

        numberemailfetch = messagescount - numberemailfetch

        print(" - Index for email : " + str(numberemailfetch))

        emaildatadict = {}

        response, message = imap.fetch(str(numberemailfetch), '(RFC822)')

        mscontent = message[0][1]

        emailmessage = email.message_from_bytes(mscontent)

        print("\n\n\n")

        headerdict = dict(emailmessage)
        headerdict["subject"] = emailmessage["subject"]

        print(" - Header data : \n\n" + str(headerdict))

        emaildatadict["header"] = headerdict

        for mspart in emailmessage.walk():

            if mspart.get_default_type() == "text/plain" or mspart.get_content_type() == "text/html":

                msbody = mspart.get_payload(decode=True)

                # msbody = (str(msbody)[:str(msbody).find(">", str(msbody).find("<body"))] + "><pre>" + str(headerdict) + "</pre>" + str(
                #     msbody)[str(msbody).find(">", str(msbody).find("<body")):]).encode('utf8')

                print("\n\n\n")

                msbody = msbody.decode()

                emaildatadict["body"] = msbody

                print(" - Body data : \n\n" + str(msbody))

        self.getinboxemaildata = emaildatadict

        return emaildatadict

    def saveemail(self):

        print(" - SAVE EMAIL ...")

        foldername = self.getinboxemaildata["header"]["subject"]

        print(" - Folder name to save email is : " + foldername)

        if not os.path.isdir(foldername):
            os.mkdir(foldername)

        with open(foldername+"/"+"index.html", "w+") as f:
            f.write(self.getinboxemaildata["body"])
            print(" - Write body in index.html file . done")
            f.close()

        with open(foldername+"/"+"header.json", "w+") as f:
            f.write(json.dumps(self.getinboxemaildata["header"]))
            print(" - Write header data in hedaer.json file . done")
            f.close()


mail = Maillepra("example@gmail.com",  # your account
                 "password")  # password

# - For Send Email :
# mail.preparationforsendemail()
# mail.sendemail()

#  - For Save Email :
# mail.getinbox()
# mail.saveemail()


class instabot:
<<<<<<< HEAD
    def __init__(self, executable_path, hidebrowser=False):

        browser_options = Options()

        if hidebrowser:
            browser_options.add_argument('--headless')

        self.browser = webdriver.Firefox(
            executable_path=executable_path, options=browser_options)
=======
    def __init__(self, executable_path):
        self.browser = webdriver.Firefox(executable_path=executable_path)
>>>>>>> ef9cfe0ac050e8d50ee9cb27d403c15f82a3a4c6

    def login(self, username, password):

        self.username = username
        self.password = password

        self.instaloginurl = "https://www.instagram.com/accounts/login/"

        print(" - Start Bot ...")

        print(" - Getting login page | Loading ...")

        self.browser.get(self.instaloginurl)

        sleep(2)

        try:
            username_input = self.browser.find_element_by_css_selector(
                "input[name='username']")
            password_input = self.browser.find_element_by_css_selector(
                "input[name='password']")
            submit_button = self.browser.find_element_by_xpath(
                "//button[@type='submit']")

            username_input.send_keys(username)
            password_input.send_keys(password)
            submit_button.click()

            print(" - You have logged in successfully")

        except:

            print(" - You were not logged in successfully ||")

        sleep(15)
        # self.browser.get("https://www.instagram.com/accounts/onetap/")

    def getuserpage(self, user):

        print(" - Getting user page | loading ...")

        self.targetusername = user

        self.userpageurl = "https://www.instagram.com/{}/".format(user)

        try:
            self.browser.get(self.userpageurl)

            print(" - The user page has been fetched successfully")

        except:

            print(" - The user page was not successfully fetched")

    def getpost(self, posturl):

        print(" - Getting post | loading ...")

        try:
            self.browser.get(posturl)

            print(" - The post has been fetched successfully")
        except:
            print(" - The post was not successfully fetched")

    def getpostowner(self):

        try:
            post_owner = self.browser.find_element_by_css_selector(
                ".sqdOP.yWX7d._8A5w5.ZIAjV").text
            return f" - This is posted under the username {post_owner}"
        except:
            return " - Can't find username .!"

    def getlikepostbool(self):

        sleep(2)

        likestatus = None

        # "span.fr66n button.wpO6b[type='button'] .QBdPU .FY9nT svg"

        # "span.fr66n button.wpO6b[type='button']"
        try:
            likertext = self.browser.find_element_by_css_selector(
                "span.fr66n button.wpO6b[type='button'] .QBdPU span svg").get_attribute("aria-label").lower()

            if likertext == "like":
                likestatus = False
            elif likertext == "unlike":
                likestatus = True
            return likestatus

        except:
            return "stop"

    def likepost(self, boollike):

        print(" - Liking ...")

        like_button = self.browser.find_element_by_css_selector(
            "span.fr66n button.wpO6b[type='button']")

        if self.getlikepostbool() == True:

            if not boollike:
                like_button.click()
                print(" - Removing like sign")
        else:
            if boollike:
                like_button.click()
                print(" - Adding like sign")

    def commentpost(self, commentlist, countforrepeatcomment=1):

        print(" - Commenting ...")

        comment_count = 0

        post_owner = self.getpostowner()

        print(f" - This is posted under the username {post_owner}")

        if self.getlikepostbool() == True:
            liketext = "like"
        else:
            liketext = "unlike"

        print(f" - You put a {liketext} sign in this post")

        print(" - Start making comments ...")

        for i in range(countforrepeatcomment):

            random.shuffle(commentlist)

            for commenttext in commentlist:

                comment_input = self.browser.find_element_by_css_selector(
                    "textarea[aria-label='Add a comment…']")

                sleep(8)

                self.browser.execute_script(
                    """document.querySelector("textarea[aria-label='Add a comment…']").value = ''""")

                # click on textarea/comment box and enter comment
                (
                    ActionChains(self.browser)
                    .move_to_element(comment_input)
                    .click()
                    .send_keys(commenttext + Keys.RETURN)
                    .perform()

                )

                print(f"#{comment_count} - {commenttext}")

                print(" - Posting comment ...")

                comment_count += 1

                if comment_count % 5 == 0:
                    print(" - Sleeping ( 20 ) seconds ...")
                    sleep(20)

                if comment_count % 15 == 0:
                    print(" - Sleeping ( 40 ) seconds ...")
                    sleep(40)

    def likeandcommentallposts(self, commentlist, boollike, countforrepeatcomment=1, countforrepeatallfn=1):
        #    , commentlist, countforrepeatecomment, boollike

        for i in countforrepeatallfn:

            print(" - Getting all posts | Loading ...")

            sleep(8)

            allposts = self.browser.find_elements(
                By.CSS_SELECTOR, "div.v1Nh3.kIKUG._bz0w")

            for postdiv in allposts:

                # open post :
                print(" - Opening post")
                postdiv.click()

                sleep(8)

                # set like sign :
                self.likepost(boollike)

                # loop cooment :
                self.commentpost(commentlist, countforrepeatcomment)

                sleep(2)

                # close post :
                print(" - Closing post")
                # close_div = self.browser.find_element_by_css_selector(
                #     "div._2dDPU.CkGkG[role='dialog']")

                close_button = self.browser.find_element_by_css_selector(
                    ".Igw0E.IwRSH.eGOV_._4EzTm.BI4qX.qJPeX.fm1AK.TxciK.yiMZG button.wpO6b[type='button']")

                # ".Igw0E.IwRSH.eGOV_._4EzTm.BI4qX.qJPeX.fm1AK.TxciK.yiMZG button.wpO6b[type='button']"
                close_button.click()

                sleep(2)

                allposts = self.browser.find_elements(
                    By.CSS_SELECTOR, "div.v1Nh3.kIKUG._bz0w")

                print(" - Sleeping ( 20 ) seconds ...")
                sleep(20)


insta = instabot("geckodriver.exe")

insta.login("username",  # username
            "password")  # password
<<<<<<< HEAD

=======
>>>>>>> ef9cfe0ac050e8d50ee9cb27d403c15f82a3a4c6

# insta.getpost("")  # url post

# insta.likepost(True)  # set like for post (True) else (false)

insta.getuserpage("s3q.x")

insta.likeandcommentallposts(["🧡🧡.", "💛💛.", "❤️❤️.", "🖤🖤.", "👌👌.",
                              "💜💜.", "💙💙.", "💚💚.", "💯🔥.", "😍😍."], True)

# insta.commentpost(["🧡🔥🔥.", "💛🔥🔥.", "❤️🔥🔥.", "🖤🔥🔥.", "👌😍😍.",
#                    "💜🔥🔥.", "💙🔥🔥.", "💚🔥🔥.", "💯🔥🔥.", "😍🔥🔥."],  # comment list

#                   3)  # count for repeat comment
